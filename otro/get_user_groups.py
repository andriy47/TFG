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
access_token = 'EAACEdEose0cBAP7P6Jc2qEmuKZCVebu0BZB2w0wKtp3yUZB1SZC3qohHqD8mVwSsCE2TmwijiaE3Ulm2yTXSTlaHqRVmRKMfAFzzsg2Qs4ifOqMlZAm9xNRjWoIGT00V3lAse7ZC3AlmAecDAZAVJVQ1PoTje3FZCJXs0M64USLe2CZARfivZCdT0hE6my6zPAzVIZD'

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
