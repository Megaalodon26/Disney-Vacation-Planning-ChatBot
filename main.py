# main.py
# Disney Planning ChatBot - improved: confidence checks, reset, JSONL logging, in-session corrections

import chatterbot.logic
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import nltk, json, os
from pathlib import Path

from storage import JsonlLogger  # new logger module

# ---- Config ----
TRAINING_FILE = "training_data.json"
DB_FILE = "database.sqlite3"   # sqlite DB for ChatterBot storage
JSONL_LOG = "conversations.jsonl"
LOW_CONFIDENCE_THRESHOLD = 0.50  # adjust as needed
# ----------------

class ChatBotTrainer:
    def __init__(self, name, training_data_file=TRAINING_FILE, db_file=DB_FILE):
        self.name = name
        self.training_data_file = training_data_file
        self.chatbot = None
        self.db_file = db_file
        self.database_uri = f"sqlite:///{self.db_file}"

    def download_nltk_data(self):
        nltk.download('punkt', quiet=True)

    def load_training_data(self):
        if not os.path.exists(self.training_data_file):
            raise FileNotFoundError(f"The file {self.training_data_file} does not exist.")

        if os.path.getsize(self.training_data_file) == 0:
            raise ValueError(f"The file {self.training_data_file} is empty.")

        with open(self.training_data_file, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON from file {self.training_data_file}: {e}")

        conversations = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, list) and len(item) >= 2:
                    conversations.append([str(item[0]), str(item[1])])
                elif isinstance(item, dict) and "input" in item and "response" in item:
                    conversations.append([str(item["input"]), str(item["response"])])
                else:
                    # ignore malformed entries
                    continue
        else:
            raise ValueError("training_data.json must be a list of pairs or objects with input/response")

        return conversations

    def initialize_and_train_chatbot(self):
        if self.chatbot is None:
            # Configure ChatBot with a specific database file for easy reset
            self.chatbot = ChatBot(
                self.name,
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                database_uri=self.database_uri,
                logic_adapters=[
                    'chatterbot.logic.BestMatch',
                ],
                read_only=False,
            )

        # Load and train with data
        training_data = self.load_training_data()
        trainer = ListTrainer(self.chatbot)
        for conv in training_data:
            trainer.train([str(s) for s in conv])

    def get_chatbot(self):
        if self.chatbot is None:
            self.initialize_and_train_chatbot()
        return self.chatbot

    def train_pair(self, user_input, bot_response):
        """
        Train the chatbot on a single pair and append to the training JSON file.
        """
        append_item = [user_input, bot_response]
        data = []
        if os.path.exists(self.training_data_file):
            with open(self.training_data_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []

        data.append(append_item)
        with open(self.training_data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Train in-memory for immediate effect
        trainer = ListTrainer(self.chatbot)
        trainer.train([user_input, bot_response])

    def reset_database(self):
        """
        Remove the sqlite database file and reinitialize the chatbot instance.
        """
        if os.path.exists(self.db_file):
            try:
                os.remove(self.db_file)
            except Exception as e:
                print(f"Warning: could not delete DB file {self.db_file}: {e}")

        # Force reinitialization
        self.chatbot = None
        self.initialize_and_train_chatbot()


class ChatBotHandler:
    def __init__(self, trainer: ChatBotTrainer, logger: JsonlLogger, low_confidence_threshold=LOW_CONFIDENCE_THRESHOLD):
        self.trainer = trainer
        self.chatbot = trainer.get_chatbot()
        self.logger = logger
        self.low_conf = low_confidence_threshold
        self._last_user_input = None

    def handle_user_input(self):
        print("Hi there! I'm PlannerBot. Commands: /reset (clear DB), /correct <answer> (teach), /exit")
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ['/exit', 'quit', 'q']:
                print("PlannerBot: No problem, cya real soon!")
                break

            if user_input.lower() == '/reset':
                print("PlannerBot: Resetting conversation storage and reinitializing — this may take a moment...")
                self.trainer.reset_database()
                self.chatbot = self.trainer.get_chatbot()
                print("PlannerBot: Done. Conversation storage reset.")
                continue

            if user_input.startswith("/correct "):
                if not self._last_user_input:
                    print("PlannerBot: I don't have a question to attach that correction to. Ask a question first.")
                    continue
                corrected_answer = user_input[len("/correct "):].strip()
                if corrected_answer:
                    self.trainer.train_pair(self._last_user_input, corrected_answer)
                    print("PlannerBot: Thanks — I've been taught that response.")
                else:
                    print("PlannerBot: Please provide the corrected answer after /correct")
                continue

            try:
                response = self.chatbot.get_response(user_input)
                conf = getattr(response, "confidence", None)
                if conf is not None and conf < self.low_conf:
                    print(f"PlannerBot: (low confidence: {conf:.2f}) {response}")
                    print("PlannerBot: If that answer is wrong, you can teach me with: /correct <correct answer>")
                else:
                    print(f"PlannerBot: {response}")

                # Save record to JSONL
                try:
                    self.logger.append(user_input, str(response), confidence=conf, metadata={"source": "chatterbot"})
                except Exception as e:
                    print(f"PlannerBot: Warning: could not write to log file: {e}")

                self._last_user_input = user_input

            except Exception as e:
                print(f"Error getting response from PlannerBot: {e}")
                try:
                    self.logger.append(user_input, f"ERROR: {e}", confidence=0.0, metadata={"error": True})
                except Exception:
                    pass


if __name__ == "__main__":
    trainer = ChatBotTrainer('PlannerBot', training_data_file=TRAINING_FILE, db_file=DB_FILE)
    trainer.download_nltk_data()
    chatbot = trainer.get_chatbot()

    logger = JsonlLogger(JSONL_LOG)
    handler = ChatBotHandler(trainer, logger)
    handler.handle_user_input()