from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import configparser
import random
from reply import responsebot
import sys

mobile_emulation = {"deviceName": "Nexus 5"}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

class InstaBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = 'https://www.instagram.com/'
        self.driver = webdriver.Chrome('./driver/chromedriver.exe',options=chrome_options)  #Chromedriver ver 87.
        self.login()

    def login(self):
        try:
            self.driver.get('{}accounts/login/'.format(self.base_url))
            sleep(1)
            self.driver.find_element_by_name('username').send_keys(self.username)
            self.driver.find_element_by_name('password').send_keys(self.password)
            login_btn = self.driver.find_element_by_xpath('//button[@type="submit"]')
            login_btn.click()
            sleep(4)
            print("Login Success!")
        except Exception as e:
            print("LOGIN FAILED! - ",e) 
    
    def nav_user(self, user):
        try:
            self.driver.get('{}{}/'.format(self.base_url, user))
            sleep(2)
        except Exception as e:
            print("UNABLE TO FIND TARGET! - ",e) 

    def follow_user(self, user):
        self.nav_user(user)
        """follow_btns = self.driver.find_elements_by_xpath("//*[text()='Follow']")

        if follow_btns:
            for btn in follow_btns:
                btn.click()
            print("Followed - ",user)
        else:
            print("Already following",user,".")
        sleep(1)"""

    def last_message(self):
        chatbox = self.driver.find_elements_by_xpath("/html/body/div[1]/section/div[2]/div/div/div[1]/div")
        mlist = []
        for message in chatbox:
            mlist.append(message.text)
        messages =  str(mlist[-1]) # string of all message
        lis = messages.split('\n') # list of all message
        last_message = lis[-1] # last message
        return last_message

    def message_user(self,user):
        self.nav_user(user)
        sleep(4)
        try:
            self.driver.find_elements_by_xpath("//*[text()='Message']")[0].click()
            sleep(2)
            message_box = self.driver.find_element_by_xpath("//textarea[@placeholder]") # message box
        except Exception as e:
            print("UNABLE TO ACCESS CHATBOX! - ",e)
        print('Sending Greeting Message..') 
        try:
            last_message = ''
            sent_message = random.choice(open("./greetings.txt").readlines())
            message_box.send_keys(sent_message)
            sleep(3)
            self.driver.find_element_by_xpath("//button[text()='Send']").click()
            sent_message = self.last_message()
            print("BOT: ",sent_message)
        except Exception as e:
            print("UNABLE TO SEND GREETING! - ",e)

        print("Press Ctrl+C to stop!")
        try:
            while True:
                current_message = self.last_message()
                if current_message != last_message and current_message != 'Typing...' and current_message != sent_message and current_message != 'Seen':
                    print(user,": ",current_message)
                    bot_response = resbot.botresponse(current_message)
                    message_box.send_keys(bot_response)
                    sleep(3)
                    self.driver.find_element_by_xpath("//button[text()='Send']").click()
                    last_message = bot_response
                    print("BOT: ",last_message)
                sleep(5)
        except KeyboardInterrupt:
            pass

        print("\n---Chat Success!---")

if __name__ == '__main__':

    # READING config.ini 
    config = configparser.ConfigParser()
    config.read('./config.ini')
    username = config['AUTH']['USERNAME']
    password = config['AUTH']['PASSWORD']
    if len(sys.argv) == 2:
        target =  sys.argv[1]
    else: 
        target = input('TARGET IG ID: ')
    resbot = responsebot()
    ig_bot = InstaBot(username, password)
    ig_bot.message_user(target)