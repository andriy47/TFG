import facebook
import requests
import json
import datetime
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['analistics']

db.resultsgroups.update_one(
{
	"dat" : "123"
},
{
	"$set" : {"date" : datetime.datetime.now().date().isoformat() }
},
	upsert=True
)

result = db.resultsgroups.find_one({"dat":"123"})

2015-12-08T18:22:38+0000

if result.get('date') == datetime.datetime.now().date().isoformat():
	print(datetime.datetime.now().date().isoformat()) 

