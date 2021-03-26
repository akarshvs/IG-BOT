
from chatterbot import ChatBot

class responsebot:
    def __init__(self):
        self.botname = 'AKARSH'
        self.chatbot = ChatBot(self.botname)

    def botresponse(self,message):
    # Get a response
        response = self.chatbot.get_response(message)
        return str(response)