import facebook
import json


from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth
from pymongo import MongoClient
from django.shortcuts import render_to_response

client = MongoClient('localhost', 27017)
db = client['analistics']


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def datag(request):
    access_token = 'EAACEdEose0cBAEZBzNXenTQyVHC4ouaqmMZCIAqFvCM2leloGQLedWIrdoRGx7nw9HnqvgZAcCAojRcPZCiADnQilxJMtRww5HB1prlYFUe2IN55oq8In82dZAaQfppVmS1UwZAqtZBLDe4h9P8c7Yo0B8ZC4LpCQu5JfdbmTfJjhp28MG9WGZCUjMFyEURmEZCfMZD'
    user = '1469643709723274'
    graph = facebook.GraphAPI(access_token)
    id_group = '1038566552861343'
    ladate = {}
    datass = graph.get_connections(id_group, 'feed', limit=50)
    for dat in datass['data']:
    	data2 = graph.get_connections(dat['id'], 'comments', limit=50)
    	data2 = data2['data']
    	if data2:
    		for value in data2:
    			com1 = value['message']
    			com1_id = value['id']
    			data3 = graph.get_connections(value['id'], 'comments', limit=50)
    			# if data3:
    			# 	for val in data3['data']:
                #
    			# 		com2_time = val1['created_time']
                #         com2 = val1['message']
                        ladate[com1_id] = com1
					# com2_id = val['id']
                        # ladate[com1_id] = com1
                        # ladate[com2_id] = val['message']
    return render(request, 'core/datag.html', {
        'ladate': ladate
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
    access_token = 'EAACEdEose0cBAEZBzNXenTQyVHC4ouaqmMZCIAqFvCM2leloGQLedWIrdoRGx7nw9HnqvgZAcCAojRcPZCiADnQilxJMtRww5HB1prlYFUe2IN55oq8In82dZAaQfppVmS1UwZAqtZBLDe4h9P8c7Yo0B8ZC4LpCQu5JfdbmTfJjhp28MG9WGZCUjMFyEURmEZCfMZD'
    graph = facebook.GraphAPI(access_token)
    print(facebook_login.extra_data)
    #user_id=facebook_login.extra_data['id']
    user_id = '786814664672852'
    profile = graph.get_object(user_id)

    #Check if user are yet in DataBase
    result_user = db.users.find_one({'id':user_id})

    #Insert if not exist
    if str(result_user) == 'None':
	       db.users.insert(profile)

    print(user_id)
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

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form})
