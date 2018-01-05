#Author: Daniel Gisolfi
#Date: 1/3/18
#GroupMe Chatbot
#v111

import os
import json
import random
import re
import sys

from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer


app = Flask(__name__)

bot = ChatBot("Marty",
	silence_performance_warning=True)
	# trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
	# storage_adapter="chatterbot.storage.SQLStorageAdapter")

@app.route('/', methods=['POST'])

def webhook():
	data = request.get_json()

	if data['name'] != 'Marty':
		methodController(data)

	return "ok", 200


def methodController(data):
 
	originalWords = re.sub("[^\w]", " ",  data['text']).split()
	words = []

	greetings = [
		"Hello",
		"Hey",
		"Hi there",
		"Hi",
		"Hallo"
		"Cheerio",
		"Cheers"
	]

	for word in originalWords:
		words.append(word.lower())

	if "marty" in words:
		if greetings in words:
			greetReply(data, greetings)

		elif"echo" in words: 
			echo(data)
		elif "create" in words:
			create(words)
		else:
			converse(data)

def create(words):
	if "list" in words:
		#find the index of the word list wich preceeds with name of the list
		x = words.index("list")

		#add 1 to the index of x so that x is equal to the index of the nameo f the list that mus be created
		x += 1

		listName = words[x]
		msg = "Okay, I have created a list called " +  listName
		sendMessage(msg)

	elif "help" in words:
		msg = "to create a list type 'create List' and then the list name. EX: Create list ToDoList"
		sendMessage(msg)

def converse(data):

	bot.set_trainer(ListTrainer)
	bot.train([
		"How are you doing?",
		"I'm doing great."])

	bot.train(
		["What is your name?",
		"My name is Marty"])

	bot.train(
		["Who made you?",
		"Daniel Gisolfi"])


	# bot.train("chatterbot.corpus.english");
	
	msg = bot.get_response(data['text'])
	sendMessage(msg)

def greetReply(data, greetings):
	name = re.sub("[^\w]", " ",  data['name']).split()
	firstName = name[0]

	#Get the number of elesments in the list
	maxLen = len(greetings)

	#get a random index from 0 to the largest index in list
	x = random.randint(0,maxLen)

	#create a message using the random item from the list plus the user's name 
	msg = greetings[x] + " " +  firstName
	sendMessage(msg)

def echo(data):
	msg = '{}, you sent "{}".'.format(data['name'], data['text'])
	sendMessage(msg)


def sendMessage(msg):

	url  = 'https://api.groupme.com/v3/bots/post'

	data = {
		'bot_id' : os.getenv('GROUPME_BOT_ID'),
		'text'   : msg,
		}
		
	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()

def log(msg):
	print(str(msg))
	sys.stdout.flush()
