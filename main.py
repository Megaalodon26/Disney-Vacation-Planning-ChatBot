from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new instance of a ChatBot
chatbot = ChatBot('PlannerBot')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english")

# Get a response to an input statement
chatbot.get_response("Hello, how are you today?")

# Train the chatbot with a list of conversations
training_data = [
    "Hi, how are you?",
    "I am good, thank you!",
    "What is your name?",
    "My name is Planner Bot.",
    "Nice to meet you, Planner Bot.",
    "Nice to meet you too!"
]

trainer.train(training_data)