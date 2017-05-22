"""
A simple example script to get all posts on a user's timeline.
"""

import facebook
import requests
import json
import pprint

from collections import OrderedDict
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['analistics']
access_token = 'EAACEdEose0cBAGpz6DZAL8AmIgUTuZCJMsMXG6NTSwMGedhY3WxIYvOgJjVeoUZAJggBTgdFU54vc0My6ROm6KR9fPqoplzgwNw3m0P5d4i1cNdkJKeYsgNRjZBTmPZB2f5qF9q1ejLB98qp0v45tRCBAhgwYOOF47P50GYm1ZAtx5vPfiyUOCoBs0pLuS2EkZD'
mesage = dict()
user = '1469643709723274'
graph = facebook.GraphAPI(access_token)
id_group = '1038566552861343'
datass = graph.get_connections(id_group, '?fields=feed{comments{message,from}}')
datass = datass.get('feed')
print('########################## COMMENTS #############################')
while(True):
	try:
		for dat in datass.get('data'):
			datt = dat.get('comments')
			if datt:
				for allcoments in datt.get('data'):
					id_user = allcoments.get('from').get('id')
					user_message = allcoments.get('message').split()
					if id_user in mesage:
						mesage[id_user].append(user_message)
					else:
						mesage[id_user] = user_message
		if datass:
			datass = requests.get(datass['paging']['next']).json()
	except KeyError:
		break
print(mesage)

print('########################## REPLYS #############################')
#comments = graph.get_connections(id_group, '?fields=feed{comments{comments}}', limit=50)
comments = graph.get_connections(id_group, '?fields=feed{comments{comments}}')
# print(comments)
repComment = dict()
comments = comments.get('feed')
# while(True):
# 	try:
# 		for val in comments.get('data'):
# 			if val.get('comments'):
# 				if val.get('comments').get('data')[0].get('comments'):
# 					for replys in val.get('comments').get('data')[0].get('comments').get('data'):
# 						id_com_usr = replys.get('from').get('id')
# 						mess_usr = replys.get('message').split()
# 						if id_com_usr in repComment:
# 							repComment[id_com_usr].append(mess_usr)
# 						else:
# 							repComment[id_com_usr] = mess_usr
# 		# print(comments)
# 		if comments:
# 			comments = requests.get(comments.get('paging')['next']).json()
# 	except TypeError:
# 		break

print(repComment)
