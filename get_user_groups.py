"""
A simple example script to get all posts on a user's timeline.
Originally created by Mitchell Stewart.
<https://gist.github.com/mylsb/10294040>
"""

import facebook
import requests
import json

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['analistics']


# You'll need an access token here to do anything.  You can get a temporary one
# here: https://developers.facebook.com/tools/explorer/
access_token = 'EAAFyTpj7GjQBAGIq4z85IsiAKJKB9XWrV5OFJq8ZAwo8sEHlpP8ZBzhqfA2ZAmExtGnFsiMhB5pLa3bMAxeiYquvBDVcZB8x5Mk2pL3guoZAdFJha870x6yf2boYTLA8wpGUkDf17F2xEoSqduBRnJK5RhANTByLjzup4udW6OtarOlQY4Je3KxY4MZAXnqdcZD'
# Look at Bill Gates's profile for this example by using his Facebook id.
#user = '1469643709723274'
user = '100009862202576'
graph = facebook.GraphAPI(access_token)
#groups = graph.get_object(id='1430450483863801', fields='feed{comments{message}}')
profile = graph.get_object(user)
groups = graph.get_connections(user, 'groups')

#Add user to mongo collection
print(profile)
result_user = db.users.find_one({'id':profile['id']})
print(result_user)
if str(result_user) == 'None':
	db.users.insert(profile)

#Add user_id wich groups is had
for value in groups['data']:
	result = db.groups.find_one({'id':value['id']})
	if str(result) == 'None':
		value['user_id'] = user
		db.groups.insert(value)
print("All done.")


