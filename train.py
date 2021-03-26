from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import pathlib
from reply import responsebot

if __name__ == "__main__":
    chat = responsebot()
    trainer = ChatterBotCorpusTrainer(chat.chatbot)
    trainer.train( str(pathlib.Path().absolute())+'/convo_samples/',)