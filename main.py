# Disney Planning ChatBot
import chatterbot.logic
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import nltk, json, os, sqlite3

# Load the training data from the JSON file
with open('training_data.json', 'r') as file:
    training_data = json.load(file)

# Connect to the SQLite3 database (or create it if it doesn't exist)
conn = sqlite3.connect('training_data.sqlite3')
cursor = conn.cursor()

# Create the training_data table
cursor.execute('''
CREATE TABLE IF NOT EXISTS training_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input TEXT NOT NULL,
    response TEXT NOT NULL
)
''')

# Insert the training data into the training_data table
for pair in training_data:
    cursor.execute('''
    INSERT INTO training_data (input, response)
    VALUES (?, ?)
    ''', (pair[0], pair[1]))

# Commit the changes and close the connection
conn.commit()
conn.close()

# Create ChatBotTrainer class to initialize the chatbot and handle training
class ChatBotTrainer:
    def __init__(self, name, training_data_file, database_uri='sqlite:///database.sqlite3'):
        self.name = name
        self.training_data_file = training_data_file
        self.database_uri = database_uri
        self.chatbot = None

    # Download the punkt tokenizer
    def download_nltk_data(self):
        nltk.download('punkt')

    def load_training_data(self):
        if not os.path.exists(self.training_data_file):
            raise FileNotFoundError(f"The file {self.training_data_file} does not exist.")

        if os.path.getsize(self.training_data_file) == 0:
            raise ValueError(f"The file {self.training_data_file} is empty.")

        with open(self.training_data_file, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON from file {self.training_data_file}: {e}")

    def initialize_and_train_chatbot(self):
        if self.chatbot is None:
            self.chatbot = ChatBot(
                self.name,
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                database_uri=self.database_uri,
                logic_adapters=[
                    'chatterbot.logic.BestMatch',
            ]
        )

        training_data = self.load_training_data()
        trainer = ListTrainer(self.chatbot)
        trainer.train(training_data)

    def get_chatbot(self):
        if self.chatbot is None:
            self.initialize_and_train_chatbot()
        return self.chatbot


# Create ChatBotHandler class to handle interactions and responses
class ChatBotHandler:
    def __init__(self, chatbot):
        self.chatbot = chatbot

    def handle_user_input(self):
        print("Hi there! I'm Oswald the Lucky PlannerBot, how can I help?")
        while True:
            user_input = input("You: ").lower() # Convert to lowercase
            if user_input in ['thank you', 'thanks']:
                print("Oswald: No problem, cya real soon!")
                break
            else:

                try:
                    response = self.chatbot.get_response(user_input)
                    print(f"Oswald the Lucky PlannerBot: {response}")
                except Exception as e:
                    print(f"Error getting response from Oswald: {e}")

# Convert training_data into a list of dictionaries
training_data_dicts = [{"input": pair[0], "response": pair[1]} for pair in training_data]

# Write the training data dictionary to a JSON file
with open('training_data.json', 'w') as file:
    json.dump(training_data, file, indent=4)

if __name__ == "__main__":
    trainer = ChatBotTrainer('Oswald the Lucky PlannerBot', 'training_data.json')
    trainer.download_nltk_data()
    chatbot = trainer.get_chatbot()

    handler = ChatBotHandler(chatbot)
    handler.handle_user_input()


