"""
A simple example script to get all posts on a user's timeline.
"""
#Imports for xlsx File.
import openpyxl
import operator

#Imports for GET data from Facebook and parse json.
import facebook
import requests
import json
import pprint

#Requirements to connect at MongoClient.
from collections import OrderedDict
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['analistics']

#Temporal tokens to use.
access_token = 'EAACEdEose0cBAAhyb20g9DwlagCh0srLZBbkUM8f5hfZATE2O2ZB3KttOgFuYZCn9O6coy1lZA3tGqm1rl7gnCLboPGWDTTWeArZC3cng6EOjNsglPSwJYCUGgbnc7dyLFgEpOUOO8TRZAnaS6cCHD9JQeLwKhT4dp8HaVI1enhJgoREuiQffo7SOzu2AOCm3MZD'
#user = '1469643709723274'
id_group = '1038566552861343'

mesage = dict()
graph = facebook.GraphAPI(access_token)

#Start to GET all comments from posts with diferents levels of Facebook groups.
datass = graph.get_connections(id_group, '?fields=feed{comments{message,from}}')
datass = datass.get('feed')
while(True):
	try:
		for dat in datass.get('data'):
			datt = dat.get('comments')
			if datt:
				for allcoments in datt.get('data'):
					id_user = allcoments.get('from').get('id')
					user_message = allcoments.get('message').split()
					if id_user in mesage:
						d = mesage.get(id_user) + user_message
						mesage[id_user] = list(set(d))
					else:
						mesage[id_user] = user_message
		if datass:
			datass = requests.get(datass['paging']['next']).json()
	except KeyError:
		break

#Start to GET all reply comments from posts of Facebook groups.
comments = graph.get_connections(id_group, '?fields=feed{comments{comments}}')
comments = comments.get('feed')
while(True):
	try:
		for val in comments.get('data'):
			if val.get('comments'):
				if val.get('comments').get('data')[0].get('comments'):
					for replys in val.get('comments').get('data')[0].get('comments').get('data'):
						id_com_usr = replys.get('from').get('id')
						mess_usr = replys.get('message').split()
						if id_com_usr in mesage:
							t = mesage.get(id_com_usr) + mess_usr
							mesage[id_com_usr] = list(set(t))
						else:
							mesage[id_com_usr] = mess_usr
		if comments:
			comments = requests.get(comments.get('paging')['next']).json()
	except TypeError:
		break
#FINAL ARRAYHASH WITH ALL COMMENTS AT PERSONS
#print(json.dumps(mesage))
print("1st Done!")

wb = openpyxl.Workbook()
wb = openpyxl.load_workbook(filename = 'emotions.xlsx', read_only=True)

sheets = wb.sheetnames
ws = wb[sheets[0]]
diccionary = dict()

#Read de xlsx file and save in arrayhash the words and her puntuation in the table.
for row in ws.iter_rows(min_row=2, max_col=11, max_row=14183):
    diccionary[row[0].value] = []
    for cell in row:
        if not cell.value in diccionary:
            diccionary[row[0].value].append(cell.value)

print('2nd Done!')
sentimientos = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for key, valu in mesage.iteritems():
	for pal in valu:
		if pal in diccionary:
			sentimientos = map(operator.add, sentimientos, diccionary.get(pal))


print(sentimientos)
