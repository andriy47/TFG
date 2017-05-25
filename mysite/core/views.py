import facebook
import json
import requests
import openpyxl
import operator

from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth
from pymongo import MongoClient
from django.shortcuts import render_to_response

from mysite.form import InputNumeroForm

client = MongoClient('localhost', 27017)
db = client['analistics']


# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             user = authenticate(
#                 username=form.cleaned_data.get('username'),
#                 password=form.cleaned_data.get('password1')
#             )
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/signup.html', {'form': form})

@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def datag(request):
    access_token = 'EAACEdEose0cBADHPGy14tAGWZCKwpYGBTvDqGxEZCgcjjgJz3mfmxpv8woRDZCRVqHExoIie9ZCkSbovmbzDrnEjrJ46vZAG1ZAehWwr0daVFZBiwFSaJ8whbP7iKOeGoji8oepuypH3GTivcGwHFS5KERRZAlMU8baoi7XGWwHN4XypxnDBFlmgjH8j5yt3XcgZD'
    if request.method == 'POST':
        if request.POST.get('numero', False):
            id_group = int(request.POST['numero'])
    #         print(m)
    # id_group = '1038566552861343'
    graph = facebook.GraphAPI(access_token)
    mesage = dict()


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
    #print("1st Done!")

    wb = openpyxl.Workbook()
    wb = openpyxl.load_workbook(filename = '/home/and/TFG/mysite/templates/registration/emotions.xlsx', read_only=True)

    sheets = wb.sheetnames
    ws = wb[sheets[0]]
    diccionary = dict()

    #Read de xlsx file and save in arrayhash the words and her puntuation in the table.
    for row in ws.iter_rows(min_row=2, max_col=11, max_row=14183):
        diccionary[row[0].value] = []
        for cell in row:
            if not cell.value in diccionary:
                diccionary[row[0].value].append(cell.value)

    #print('2nd Done!')
    sentimientos = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for key, valu in mesage.iteritems():
    	for pal in valu:
    		if pal in diccionary:
    			sentimientos = map(operator.add, sentimientos, diccionary.get(pal))

    finaldata = dict()
    typeemoji = ['Positivo','Confiado','Alegria','Anticipacion','Sopresa','Tristesa','Disgusto','Miedo','Ira','Negatividad']
    for typ, punt in zip(typeemoji,sentimientos):
        finaldata[typ] = punt

    #print(finaldata)

    return render(request, 'core/datag.html', {
        'ladate': finaldata,
    })
#     return render(request, 'core/gentelella-master/production/adminpanel.html')

@login_required
def settings(request):
    #access_token = '407156876319284|h5wEvmcAky9NjDDXXp4rnjHkFbg'
    user = request.user
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    #Get tokens and id necesry from facebook user

    #access_token = facebook_login.extra_data['access_token']
    access_token = 'EAACEdEose0cBADHPGy14tAGWZCKwpYGBTvDqGxEZCgcjjgJz3mfmxpv8woRDZCRVqHExoIie9ZCkSbovmbzDrnEjrJ46vZAG1ZAehWwr0daVFZBiwFSaJ8whbP7iKOeGoji8oepuypH3GTivcGwHFS5KERRZAlMU8baoi7XGWwHN4XypxnDBFlmgjH8j5yt3XcgZD'
    graph = facebook.GraphAPI(access_token)
    #print(facebook_login.extra_data)
    #user_id=facebook_login.extra_data['id']
    # print(user_id)
    user_id = '786814664672852'
    profile = graph.get_object(user_id)

    #Check if user are yet in DataBase
    result_user = db.users.find_one({'id':user_id})

    #Insert if not exist
    if str(result_user) == 'None':
	       db.users.insert(profile)

    #print(user_id)
    groups = graph.get_connections(user_id, 'groups')
    # data_groups = groups['data']
    # for value in data_groups:
    #     print(value['name'])
    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())


    groups_avaliables = {}
    #Add user_id wich groups is had

    for value in groups['data']:
        result = db.groups.find_one({'id':value['id']})
        groups_avaliables[value['id']]=value['name']
        #groups_avaliables.append(value['id']:value['name'])
        if str(result) == 'None':
            value['user_id'] = user
            db.groups.insert(value)
    # print(groups_avaliables)
    return render(request, 'core/settings.html', {
        'groups_avaliables': groups_avaliables,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
        })

# @login_required
# def password(request):
#     if request.user.has_usable_password():
#         PasswordForm = PasswordChangeForm
#     else:
#         PasswordForm = AdminPasswordChangeForm
#
#     if request.method == 'POST':
#         form = PasswordForm(request.user, request.POST)
#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, form.user)
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('password')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordForm(request.user)
#     return render(request, 'core/password.html', {'form': form})
