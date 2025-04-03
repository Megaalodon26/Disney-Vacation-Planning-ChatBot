# Disney Planning ChatBot
import chatterbot.logic
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import nltk, json, os

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

# Define training data
training_data = [
    ["Hi", "Hello! How can I assist you today?"],
    ["Hello", "Hi there! How can I help you?"],
    ["How are you?", "I'm just a bot, but I'm here to help you!"],
    ["What's your name?", "I'm Oswald the Lucky PlannerBot."],
    ["Thank you", "You're welcome! Have a great day!"],
    ["Thanks", "No problem! If you need anything else, just ask!"],
    ["Thanks", "You're welcome! Have a great day!"],
    ["Thanks", "No problem, cya around real soon!"],
    ["Thank you", "No problem, cya around real soon!"],
    ["Thanks", "No problem! If you need anything else, just ask!"],
    [
        "I'm going to Disney World soon. What are the best rides at Magic Kingdom?",
        "Here are my favorites: Space Mountain, TRON Lightcycle Run, Pirates of the Caribbean, "
        "Tiana's Bayou Adventure, Big Thunder Mountain RailRoad, and Buzz Lightyear's Space Ranger Spin!"
    ],
    [
        "Rides at Magic Kingdom?",
        "Here are my favorites: Space Mountain, TRON Lightcycle Run, Pirates of the Caribbean, "
        "Tiana's Bayou Adventure, Big Thunder Mountain RailRoad, and Buzz Lightyear's Space Ranger Spin!"
    ],
    [
        "I'm visiting Disney World soon. What are the top rides at Magic Kingdom?",
        "Here are my favorites: Space Mountain, TRON Lightcycle Run, Pirates of the Caribbean, "
        "Tiana's Bayou Adventure, Big Thunder Mountain RailRoad, and Buzz Lightyear's Space Ranger Spin!"
    ],
    [
        "I'm planning a trip to Disney World. What are the must-see rides at Magic Kingdom?",
        "Here are my favorites: Space Mountain, TRON Lightcycle Run, Pirates of the Caribbean, "
        "Tiana's Bayou Adventure, Big Thunder Mountain RailRoad, and Buzz Lightyear's Space Ranger Spin!"
    ],
    [
        "I'm going to Disney World soon. What are the best rides at Hollywood Studios?",
        "Here are my favorites: Mickey & Minnie's Runaway Railway, Millennium Falcon: Smuggler's Run, Slinky Dog Dash, "
        "Rock 'n' Roller Coaster Starring Aerosmith, Star Tours - The Adventures Continue, Star Wars: Rise of the Resistance, "
        "Toy Story Mania!, and The Twilight Zone Tower of Terror!"
    ],
    [
        "Rides at Hollywood Studios?",
        "Here are my favorites: Mickey & Minnie's Runaway Railway, Millennium Falcon: Smuggler's Run, Slinky Dog Dash, "
        "Rock 'n' Roller Coaster Starring Aerosmith, Star Tours - The Adventures Continue, Star Wars: Rise of the Resistance, "
        "Toy Story Mania!, and The Twilight Zone Tower of Terror!"
    ],
    [
        "I'm visiting Disney World soon. What are the top rides at Hollywood Studios?",
        "Here are my favorites: Mickey & Minnie's Runaway Railway, Millennium Falcon: Smuggler's Run, Slinky Dog Dash, "
        "Rock 'n' Roller Coaster Starring Aerosmith, Star Tours - The Adventures Continue, Star Wars: Rise of the Resistance, "
        "Toy Story Mania!, and The Twilight Zone Tower of Terror!"
    ],
    [
        "I'm planning a trip to Disney World soon. What are the must-see rides at Hollywood Studios?",
        "Here are my favorites: Mickey & Minnie's Runaway Railway, Millennium Falcon: Smuggler's Run, Slinky Dog Dash, "
        "Rock 'n' Roller Coaster Starring Aerosmith, Star Tours - The Adventures Continue, Star Wars: Rise of the Resistance, "
        "Toy Story Mania!, and The Twilight Zone Tower of Terror!"
    ],
    [
        "I'm going to Disney World soon. What are the best rides at EPCOT?",
        "Here are my favorites: Guardians of the Galaxy: Cosmic Rewind, Living with the Land, Remy's Ratatouille Adventure, "
        "The Seas with Nemo and Friends, Test Track, and Soarin' Around the World!"
    ],
    [
        "Rides at EPCOT?",
        "Here are my favorites: Guardians of the Galaxy: Cosmic Rewind, Living with the Land, Remy's Ratatouille Adventure, "
        "The Seas with Nemo and Friends, Test Track, and Soarin' Around the World!"
    ],
    [
        "I'm visiting Disney World soon. What are the top rides at EPCOT?",
        "Here are my favorites: Guardians of the Galaxy: Cosmic Rewind, Living with the Land, Remy's Ratatouille Adventure, "
        "The Seas with Nemo and Friends, Test Track, and Soarin' Around the World!"
    ],
    [
        "I'm planning a trip to Disney World soon. What are the must-see rides at EPCOT?",
        "Here are my favorites: Guardians of the Galaxy: Cosmic Rewind, Living with the Land, Remy's Ratatouille Adventure, "
        "The Seas with Nemo and Friends, Test Track, and Soarin' Around the World!"
    ],
    [
        "I'm going to Disney World soon. What are the best rides at Animal Kingdom?",
        "That's my favorite park actually. Here are my favorite rides there: Avatar Flight of Passage, Kilimanjaro Safaris, "
        "Na'vi River Journey, DINOSAUR, Expedition Everest - Legend of the Forbidden Mountain, and Kali River Rapids!"
    ],
    [
        "Rides at Animal Kingdom?",
        "That's my favorite park actually. Here are my favorite rides there: Avatar Flight of Passage, Kilimanjaro Safaris, "
        "Na'vi River Journey, DINOSAUR, Expedition Everest - Legend of the Forbidden Mountain, and Kali River Rapids!"
    ],
    [
        "I'm visiting Disney World soon. What are the top rides at Animal Kingdom?",
        "That's my favorite park actually. Here are my favorite rides there: Avatar Flight of Passage, Kilimanjaro Safaris, "
        "Na'vi River Journey, DINOSAUR, Expedition Everest - Legend of the Forbidden Mountain, and Kali River Rapids!"
    ],
    [
        "I'm planning a trip to Disney World soon. What are the must-see rides at Animal Kingdom?",
        "That's my favorite park actually. Here are my favorite rides there: Avatar Flight of Passage, Kilimanjaro Safaris, "
        "Na'vi River Journey, DINOSAUR, Expedition Everest - Legend of the Forbidden Mountain, and Kali River Rapids!"
    ],
]

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


