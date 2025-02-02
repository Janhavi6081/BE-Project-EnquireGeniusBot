#from flask import Flask, request
#import requests
#from twilio.twiml.messaging_response import MessagingResponse
#app = Flask(__name__)

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import json
import requests
import os
import random
import textsim2
chatlist=[] 
class ultraChatBot():
   
    def __init__(self, json):
        self.json = json
        self.dict_messages = json['data']
        self.ultraAPIUrl = 'https://api.ultramsg.com/instance86764/'
        self.token = 'c205ugb6klv42f3z'
        
   
    def send_requests(self, type, data):
        url = f"{self.ultraAPIUrl}{type}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()

    def send_message(self, chatID, text):
        data = {"to" : chatID,
                "body" : text}  
        answer = self.send_requests('messages/chat', data)
       
        return answer
    def send_message2(self, chatID, text):
         data = text_similarity(text)
         print(data)
         if str(data).__contains__("https://firebasestorage.googleapis.com") and (str(data).__contains__(".jpeg")):
             print("__________________image______")
             return self.send_image(chatID,str(data))
         if str(data).__contains__("https://firebasestorage.googleapis.com") and (str(data).__contains__(".mp4")):
             print("__________________video______")
             return self.send_video(chatID,str(data))
         if str(data).__contains__("https://firebasestorage.googleapis.com") and (str(data).__contains__(".mp3")):
             print("__________________audio______")
             return self.send_audio(chatID,str(data))      
         if str(data).__contains__("https://firebasestorage.googleapis.com") and (str(data).__contains__(".pdf")):
             print("__________________doc______")
             return self.send_doc(chatID,str(data))     
               
         else:
             return self.send_message(chatID, str(data))
    
    def welcome(self,chatID, noWelcome = False):
        welcome_string = ''
        if (noWelcome == False):
            welcome_string = "Hi , welcome to Enquiry Genius Bot.How may I help you? \n"
        else:
            welcome_string = "wrong command"
        print(welcome_string)    
        return self.send_message(chatID,welcome_string)
    
    def send_default(self,chatID):
        welcome_string = "I'm sorry, I couldn't understand your question."
        print(welcome_string)    
        return self.send_message(chatID,welcome_string)    
    def send_image(self, chatID,picurl):
        data = {"to" : chatID,
                "image" : picurl}  
        answer = self.send_requests('messages/image', data)
        return answer
    
    def send_video(self, chatID,picurl):
        data = {"to" : chatID,
                "video" : picurl}  
        answer = self.send_requests('messages/video', data)
        return answer

    def send_audio(self, chatID,picurl):
        data = {"to" : chatID,
                "audio" : picurl}  
        answer = self.send_requests('messages/audio', data)
        return answer
    
    def send_doc(self, chatID,picurl):
        data = {"to" : chatID,
                "document" : picurl,
                "filename":"hello.pdf",
                "caption":"doc caption"}  
        answer = self.send_requests('messages/document', data)
        return answer
        
    def Processingـincomingـmessages(self):
        if self.dict_messages != []:
            message =self.dict_messages
            text = message['body'].split()
            incoming_message=str(message['body'])
            chatID  = message['from'] 
            print(str(message['body']))
            if incoming_message=="#123":
                chatlist.append(chatID)             
                return self.welcome(chatID)          
            else: 
             print(chatlist)
             if chatID in chatlist:
              print("chat id match")
              if not message['fromMe']:                
                print(text[0].lower())
                if text[0].lower() == 'hi' or text[0].lower() == 'hii' or text[0].lower() == 'hey':
                    return self.welcome(chatID)
                else:
                    return self.send_message2(chatID,incoming_message.lower())
                
             else: return 'NoCommand'
    def Processingـmybot(incoming_message):
         data = text_similarity(incoming_message)
         print(data)
         return data
            
try:
 os.remove("database.sqlite3")
except:
 print("")

# Load your custom data from a JSON file
with open('clg.json', 'r', encoding='utf-8') as file:
    college_data = json.load(file)
# Create a new trainer for the chat bot
"""
# Now, let's interact with the bot
print("Bot: Hi, how can I assist you today?")
def text_similarity(sentence1):
    output=""
    dist=0
    for input_text, response_text in college_data:
        matching_words_count = textsim2.count_matching_words(input_text, sentence1)
        if dist<matching_words_count:
            dist=matching_words_count
            output=response_text
    if dist<1:
        output="I'm sorry, I couldn't understand your question."
    return output

"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def text_similarity(sentence1):
    # Vectorize the input sentence and the input texts from college_data
    tfidf_vectorizer = TfidfVectorizer()
    sentences = [input_text for input_text, _ in college_data]
    sentences.append(sentence1)
    tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)

    # Calculate cosine similarity between the input sentence and each input text
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # Find the index of the most similar input text
    most_similar_index = cosine_similarities.argmax()

    # Get the corresponding response text
    output = college_data[most_similar_index][1]

    return output



  