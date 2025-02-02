from flask import Flask, request, jsonify
from Bot_whatsapp4 import ultraChatBot
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        print(request.json)
        bot = ultraChatBot(request.json)
        return bot.Processingـincomingـmessages()

@app.route('/mybot', methods=['POST'])
def mybot():
    if request.method == 'POST':
        print(request.json)
        return ultraChatBot.Processingـmybot(request.json["data"])

if(__name__) == '__main__':
    app.run()