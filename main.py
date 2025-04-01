from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import nltk, json

# Download the punkt tokenizer
nltk.download('punkt')

# Define training data
training_data = [
    ["Hi", "Hi there! I'm Oswald the Lucky PlannerBot, how can I help?"],
    ["Hi!", "Hi!", "How are you?", "I'm good how are you?", "I'm doing well."],
    ["I'm going to Disney World soon. What are the best rides at Magic Kingdom?"],
    ["Here are my favorites: are Space Mountain, TRON Lightcycle Run, Pirates of the Caribbean, Tiana's Bayou Adventure, Big Thunder Mountain RailRoad and Buzz Lightyear's Space Ranger Spin!"],
    ["Thank you", "No problem! Cya real soon!"],

    ["Hi", "Hi there! I'm Oswald the Lucky PlannerBot, how can I help?"],
    ["Hi!", "Hi!", "How are you?", "I'm good how are you?", "I'm doing well."],
    ["I'm visiting to Disney World soon. What are the top rides at Magic Kingdom?"],
    ["Here are my favorites: are Space Mountain, TRON Lightcycle Run, Pirates of the Caribbean, Tiana's Bayou Adventure, Big Thunder Mountain RailRoad and Buzz Lightyear's Space Ranger Spin!"],
    ["Thank you", "No problem! Cya real soon!"],

    ["Hi", "Hi there! I'm Oswald the Lucky PlannerBot, how can I help?"],
    ["Hi!", "Hi!", "How are you?", "I'm good how are you?", "I'm doing well."],
    ["I'm planning a trip to Disney World. What are the no-skip rides at Magic Kingdom?"],
    ["Here are my favorites: are Space Mountain, TRON Lightcycle Run, Pirates of the Caribbean, Tiana's Bayou Adventure, Big Thunder Mountain RailRoad and Buzz Lightyear's Space Ranger Spin!"],
    ["Thank you", "No problem! Cya real soon!"],

    ["Hi", "Hey! I'm Oswald the Lucky PlannerBot, how can I help?"],
    ["Hi!", "Hi!", "How are you?", "I'm good how are you?", "I'm doing well."],
    ["I'm going to Disney World soon. What are the best rides at Hollywood Studios?"],
    ["Here are my favorites: Mickey & Minnie's Runaway Railway, Millennium Falcon: Smuggler's Run, Slinky Dog Dash, Rock 'n' Roller Coaster Starring Aerosmith, Star Tours - The Adventures Continue, Star Wars: Rise of the Resistence, Toy Story Mania! and The Twilight Zone Tower of Terror!"],
    ["Thank you", "No problem! Cya real soon!"],

    ["Hi", "Hey! I'm Oswald the Lucky PlannerBot, how can I help?"],
    ["Hi!", "Hi!", "How are you?", "I'm good how are you?", "I'm doing well."],
    ["I'm visiting Disney World soon. What are the top rides at Hollywood Studios?"],
    ["Here are my favorites: Mickey & Minnie's Runaway Railway, Millennium Falcon: Smuggler's Run, Slinky Dog Dash, Rock 'n' Roller Coaster Starring Aerosmith, Star Tours - The Adventures Continue, Star Wars: Rise of the Resistence, Toy Story Mania! and The Twilight Zone Tower of Terror!"],
    ["Thank you", "No problem! Cya real soon!"],

    ["Hi", "Hey! I'm Oswald the Lucky PlannerBot, how can I help?"],
    ["Hi!", "Hi!", "How are you?", "I'm good how are you?", "I'm doing well."],
    ["I'm planning a trip to Disney World soon. What are the no-skip rides at Hollywood Studios?"],
    ["Here are my favorites: Mickey & Minnie's Runaway Railway, Millennium Falcon: Smuggler's Run, Slinky Dog Dash, Rock 'n' Roller Coaster Starring Aerosmith, Star Tours - The Adventures Continue, Star Wars: Rise of the Resistence, Toy Story Mania! and The Twilight Zone Tower of Terror!"],
    ["Thank you", "No problem! Cya real soon!"],

    ["Hi", "Hey! I'm Oswald the Lucky PlannerBot, how can I help?"],
    ["Hi!", "Hi!", "How are you?", "I'm good how are you?", "I'm doing well."],
    ["I'm going to Disney World soon. What are the best rides at EPCOT?"],
    ["Here are my favorites: Guardians of the Galaxy: Cosmic Rewind, Living with the Land, Remy's Ratatouille Adventure, The Seas with Nemo and Friends, Test Track and Soarin' Around the World!"],
    ["Thank you", "No problem! Cya real soon!"],

    ["Hi", "Hey! I'm Oswald the Lucky PlannerBot, how can I help?"],
    ["Hi!", "Hi!", "How are you?", "I'm good how are you?", "I'm doing well."],
    ["I'm visiting Disney World soon. What are the top rides at EPCOT?"],
    ["Here are my favorites: Guardians of the Galaxy: Cosmic Rewind, Living with the Land, Remy's Ratatouille Adventure, The Seas with Nemo and Friends, Test Track and Soarin' Around the World!"],
    ["Thank you", "No problem! Cya real soon!"],

    ["Hi", "Hey! I'm Oswald the Lucky PlannerBot, how can I help?"],
    ["Hi!", "Hi!","How are you?", "I'm good how are you?", "I'm doing well."],
    ["I'm planning a trip to Disney World soon. What are the no-skip rides at EPCOT?"],
    ["Here are my favorites: Guardians of the Galaxy: Cosmic Rewind, Living with the Land, Remy's Ratatouille Adventure, The Seas with Nemo and Friends, Test Track and Soarin' Around the World!"],
    ["Thank you", "No problem! Cya real soon!"],

    ["Hi", "Hey! I'm Oswald the Lucky PlannerBot, how can I help?"],
    ["Hi!", "Hi!", "How are you?", "I'm good how are you?", "I'm doing well."],
    ["I'm going to Disney World soon. What are the best rides at Animal Kingdom?"],
    ["That's my favorite park actually. Here are my favorite rides there: Avatar Flight of Passage, Kilimanjaro Safaris, Na'vi River Journey, DINOSAUR, Expedition Everest - Legend of the Forbidden Mountain and Kali River Rapids!"],
    ["Thank you", "No problem! Cya real soon!"],

    ["Hi", "Hey! I'm Oswald the Lucky PlannerBot, how can I help?"],
    ["Hi!", "Hi!", "How are you?", "I'm good how are you?", "I'm doing well."],
    ["I'm visiting Disney World soon. What are the top rides at Animal Kingdom?"],
    ["That's my favorite park actually. Here are my favorite rides there: Avatar Flight of Passage, Kilimanjaro Safaris, Na'vi River Journey, DINOSAUR, Expedition Everest - Legend of the Forbidden Mountain and Kali River Rapids!"],
    ["Thank you", "No problem! Cya real soon!"],

    ["Hi", "Hey! I'm Oswald the Lucky PlannerBot, how can I help?"],
    ["Hi!", "Hi!", "How are you?", "I'm good how are you?", "I'm doing well."],
    ["I'm planning a trip to Disney World soon. What are the no-skip rides at Animal Kingdom?"],
    ["That's my favorite park actually. Here are my favorite rides there: Avatar Flight of Passage, Kilimanjaro Safaris, Na'vi River Journey, DINOSAUR, Expedition Everest - Legend of the Forbidden Mountain and Kali River Rapids!"],
    ["Thank you", "No problem! Cya real soon!"],

]

# Write the training data to a JSON file
with open('training_data.json', 'w') as file:
    json.dump(training_data, file, indent=4)

# Initialize the ChatBot
chatbot = ChatBot('Oswald the Lucky PlannerBot')

# Load training data from a JSON file
def load_training_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Create object of ChatBot class with Storage Adapter and add initialize function
def initialize_and_train_chatbot():
    local_chatbot = ChatBot(
        'Oswald the Lucky PlannerBot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///database.sqlite3',
        logic_adapters=[
            'chatterbot.logic.BestMatch'
        ]
    )

    # Load training data
    training_data = load_training_data('training_data.json')

    # Train the ChatBot
    trainer = ListTrainer(local_chatbot)
    trainer.train(training_data)
    return local_chatbot

chatbot = initialize_and_train_chatbot()

# Handle User Input
print("Hi there! I'm Oswald the Lucky PlannerBot, how can I help?")
while True:
    user_input = input("You: ").lower()  # Convert input to lowercase
    if user_input in ['thank you', 'thanks']:
        print("Oswald the Lucky PlannerBot: No problem, cya real soon!")
        break
    else:
        response = chatbot.get_response(user_input)
        print(f"Oswald the Lucky PlannerBot: {response}")


# class representing the Parks at Disney World
#class Parks:
    #def __init__(self, prompt1, prompt2, prompt3, prompt4):
        #self.prompt1 = 'Magic Kingdom'
        #self.prompt2 = 'Hollywood Studios'
        #self.prompt3 = 'EPCOT'
        #self.prompt4 = 'Animal Kingdom'

# while True:
    #if 'Magic Kingdom' in user_input:
        #print(Parks.prompt1)
    #elif 'Hollywood Studios' in user_input:
        #print(Parks.prompt2)
    #elif 'EPCOT' in user_input:
        #print(Parks.prompt3)
    #else:
        #print(Parks.prompt4)
        #break
