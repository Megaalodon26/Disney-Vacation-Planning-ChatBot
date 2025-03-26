from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Create a new instance of a ChatBot
chatbot = ChatBot('Example Bot')

# Create a new trainer for the chatbot
trainer = ListTrainer(chatbot)

# Train the chatbot with a list of conversations
training_data = [
    "Hi, how are you?",
    "I am good, thank you!",
    "What is your name?",
    "My name is Example Bot.",
    "Nice to meet you, Example Bot.",
    "Nice to meet you too!"
]

trainer.train(training_data)