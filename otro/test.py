"""
A simple example script to get all posts on a user's timeline.
"""

import facebook
import requests
import json

from collections import OrderedDict
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['analistics']
access_token = 'EAACEdEose0cBADiSQnmEDVzBBgtKQGdUeULdkNZBqMiI7mRplVv9T85EyRjfLZCX1tNQ075a66pDGZBb8nz0vZCHSVZAAllFnGpWBwU9ckcaPXegRXkR8YeVcOkaOqDyWCpk9LUzinVhMIqPYZAvfM2S6uT0nD1iHfMZA60fOkZCwCUy5479HL2WhYxMq8ZAu65sZD'

user = '1469643709723274'
graph = facebook.GraphAPI(access_token)
id_group = '1038566552861343'
datass = graph.get_connections(id_group + '/feed', '?comments{message}')
for dat in datass['data']:
	id_user = dat.get('from').get('id')
	if dat.get('message'):
		user_message = dat.get('message')
		user_message = user_message.split()
		print(user_message,id_user)
#print(datass['paging']) #Para pasar a la siguiente pagina
comments = graph.get_connections(id_group + '/feed', '?comments{comments}')
