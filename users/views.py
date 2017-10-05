# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from users.models import Users, Follow, AndroidDevice
from users.serializers import UserSerializer, UserSearchSerializer, FollowSerializer, ContactsSerializer, UserProfileSerializer, UserSerializerNew


from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .util import handle_uploaded_file, verifyToken
from django.db import IntegrityError

import feed
from feed import serializers as feed_serializers


def hello(request):
	return render(request, 'privacy.html')
   #return render(request, "hello.html", {})
# Create your views here.

@csrf_exempt
@verifyToken(forGetRequest=True, forPostRequest=False)
def user_list(request):
	"""
	List all code Userss, or create a new Users.
	"""
	if request.method == 'GET':
		u = Users.objects.all()
		serializer = UserSerializerNew(u, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = UserSerializerNew(data=data)
		if serializer.is_valid():
			serializer.save()
			mdata = serializer.data
			mdata['password'] = ""
			return JsonResponse(mdata, status=201)


		
		return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@verifyToken(forGetRequest=True, forPostRequest=True, getUsernameFromKey="username")
def update_user(request):
	"""
	List all code Userss, or create a new Users.
	"""
	if request.method == 'POST':
		data = JSONParser().parse(request)
		user = Users.objects.get(username=data['username'])
		user.name=data['name']
		user.password=data['password']
		user.status = data['status']
		user.save()

		user.password=""
		serializer = UserSerializerNew(user)
		return JsonResponse(serializer.data, status=201)






@csrf_exempt
#@verifyToken(forGetRequest=True, forPostRequest=True, getUsernameFromKey="username")
def user_login(request):

	if request.method == 'POST':

		data = JSONParser().parse(request)
		#print data
		
		try:
			user = Users.objects.get(username=data['username'], password=data['password'])
		except Users.DoesNotExist:
			return JsonResponse({'success': False, 'message': 'user not found'})

		user.password = ''
		serializer = UserSerializerNew(user)
		return JsonResponse(serializer.data)


@csrf_exempt
def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			return JsonResponse({'success': True, 'message': 'image uploaded'})
	

		return JsonResponse({'success': true, 'message': 'image uploaded'})
	return JsonResponse({'success': False, 'message': 'could not upload image'})




@csrf_exempt
def search_user(request):
	if request.method == 'GET':

		name = request.GET.get('name')
		
		try:
			users = Users.objects.filter(name__icontains=name, status='active')
		except Users.DoesNotExist:
			return JsonResponse({'success': False, 'message': 'user not found'})

		serializer = UserSearchSerializer(users, many=True)
		return JsonResponse(serializer.data, safe=False)





@csrf_exempt
@verifyToken(forGetRequest=True, forPostRequest=True, getUsernameFromKey="user")
def follow(request):

	if request.method == 'POST':

		try:

			data = JSONParser().parse(request)
			user = Users.objects.get(username=data['user'])
			following = Users.objects.get(username=data['following'])
			follow = Follow(user=user, following=following)
			follow.save()
			return JsonResponse({'success': True, 'message': 'followed', "follow_id": follow.id})

		except IntegrityError as e:
			if 'unique constraint' in e.message:
				return JsonResponse({'success': False, 'message': 'already following'})

		
	return JsonResponse({'success': False, 'message': 'some error occured'})


@csrf_exempt
@verifyToken(forGetRequest=True, forPostRequest=True, getUsernameFromKey="username")
def followMany(request):

	if request.method == 'POST':

		try:

			data = JSONParser().parse(request)
			user = Users.objects.get(username=data['username'])

			followObjList = []
			usersObjList = []

			for username in data['toFollow']:

				try:
					print str(username)
					following = Users.objects.get(username=str(username))
					followObjList.append(Follow(user=user, following=following))
				except:
					new_user = Users(name="user", username=username, password="12345678", status="inactive")
					usersObjList.append(new_user)
					new_user.save()
					followObjList.append(Follow(user=user, following=new_user))
					continue


			#Users.objects.bulk_create(usersObjList)

			#Follow.objects.bulk_create(followObjList)

			for follow_obj in followObjList:
				try:
					follow_obj.save()

				except IntegrityError as e:
					if 'unique constraint' in e.message:
						pass


			return JsonResponse({'success': True, 'message': 'followed', 'count': len(followObjList)})

		except IntegrityError as e:
			if 'unique constraint' in e.message:
				return JsonResponse({'success': False, 'message': 'already following'})

		
	return JsonResponse({'success': False, 'message': 'some error occured'})


@csrf_exempt
@verifyToken(forGetRequest=True, forPostRequest=True, getUsernameFromKey="username")
def unfollowMany(request):

	if request.method == 'POST':

			try:

				data = JSONParser().parse(request)
				user = Users.objects.get(username=data['username'])

				unfollowObjList = []

				for username in data['toUnFollow']:

					try:
						print str(username)
						following = Users.objects.get(username=str(username))
						unfollowObjList.append(following.id)
					except:
						pass


				Follow.objects.filter(user=user.id, following__in=unfollowObjList).delete()
				return JsonResponse({'success': True, 'message': 'unfollowed'})

			except IntegrityError as e:
				if 'unique constraint' in e.message:
					return JsonResponse({'success': False, 'message': 'already not following'})

			
	return JsonResponse({'success': False, 'message': 'some error occured'})




@csrf_exempt
@verifyToken(forGetRequest=True, forPostRequest=True, getUsernameFromKey="user")
def unfollow(request):

	if request.method == 'POST':

		try:

			data = JSONParser().parse(request)
			user = Users.objects.get(username=data['user'])
			following = Users.objects.get(username=data['following'])
			Follow.objects.filter(user=user, following=following).delete()
			return JsonResponse({'success': True, 'message': 'unfollowed'})

		except IntegrityError as e:
			if 'unique constraint' in e.message:
				return JsonResponse({'success': False, 'message': 'already not following'})

		
	return JsonResponse({'success': False, 'message': 'some error occured'})



@csrf_exempt
@verifyToken(forGetRequest=True, forPostRequest=False, getUsernameFromParameter='username')
def user_profile(request):

	if request.method == 'GET':
		username = request.GET.get('username')  
		followers_array=[]
		following_array=[]
		try:
			user = Users.objects.get(username=username)
			followers = Follow.objects.filter(following=user)
			for obj in followers:
				followers_array.append(obj.user.username)
			print followers_array
			following = Follow.objects.filter(user=user)

			for obj in following:
				following_array.append(obj.following.username)
			print following_array


		except Users.DoesNotExist:
			return JsonResponse({'success': False, 'message': 'user not found'})

		user.password = ''
		userserializer = UserSerializer(user)
		return JsonResponse({"user_details": userserializer.data, "followers": followers_array, "following": following_array})



@csrf_exempt
def add_user_android_device(request):


	
	if request.method == 'POST':

		try:

			data = JSONParser().parse(request)
			user = Users.objects.get(username=data['user'])

			updated, created = AndroidDevice.objects.update_or_create(
			        user=user, defaults={"device_id": data['device_id']}
			)

			if created:
				return JsonResponse({'success': True, 'message': 'device saved'})
			else:
				return JsonResponse({'success': True, 'message': 'device updated'})


		except Users.DoesNotExist:
			return JsonResponse({'success': False, 'message': 'user not found'})
		


		return JsonResponse({'success': False, 'message': 'some error occured'})


@csrf_exempt
def remove_user_android_device(request):
	
	if request.method == 'POST':

		try:

			data = JSONParser().parse(request)
			user = Users.objects.get(username=data['user'])
			AndroidDevice.objects.filter(user=user, device_id=data['device_id']).delete()

			return JsonResponse({'success': True, 'message': 'device removed'})
		except Users.DoesNotExist:
			return JsonResponse({'success': False, 'message': 'user not found'})


		return JsonResponse({'success': False, 'message': 'some error occured'})


@csrf_exempt
@verifyToken(forGetRequest=True, forPostRequest=True, getUsernameFromParameter='username')
def followers(request):

	if request.method == 'GET':
		username = request.GET.get('username')  
		followers_array=[]
		try:
			user = Users.objects.get(username=username)

			query = "SELECT users.id, name, username FROM `follow` LEFT JOIN users ON follow.user_id = users.id WHERE following_id =" + str(user.id) +  " and status = 'active'"
			followers = Users.objects.raw(query)
			print query



			serializer = UserProfileSerializer(followers, many=True)

			return JsonResponse({'success': False, 'followers': serializer.data})

		except Users.DoesNotExist:
			return JsonResponse({'success': False, 'message': 'user   not found'})



		return JsonResponse({'success': False, 'followers': []})


@csrf_exempt
@verifyToken(forGetRequest=True, forPostRequest=True, getUsernameFromParameter='username')
def following(request):

	if request.method == 'GET':
		username = request.GET.get('username')  
		followers_array=[]
		try:
			user = Users.objects.get(username=username)

			#query = "SELECT users.id, name, username FROM `follow` LEFT JOIN users ON follow.following_id = users.id WHERE user_id =" + str(user.id) +  " and status = 'active'"
			query = "SELECT users.id, name, username, status FROM `follow` LEFT JOIN users ON follow.following_id = users.id WHERE user_id =" + str(user.id) +  " and CHAR_LENGTH(username) = 10"
			followers = Users.objects.raw(query)
			print query



			serializer = ContactsSerializer(followers, many=True)

			return JsonResponse({'success': False, 'following': serializer.data})

		except Users.DoesNotExist:
			return JsonResponse({'success': False, 'message': 'user   not found'})



		return JsonResponse({'success': False, 'following': []})


@csrf_exempt
def registeredUsers(request):
		if request.method == 'POST':

			try:
				data = JSONParser().parse(request)
				usernamesList = data['usernames']


				query = "SELECT users.id, username FROM users where username in ( " +  ','.join(['"'+uname+'"' for uname in usernamesList])  + " ) "
				print query


				registered_users_obj = Users.objects.raw(query)

				registeredUsersList = []

				for obj in registered_users_obj:
					registeredUsersList.append(obj.username)

				return JsonResponse({'success': True, 'registered_users': registeredUsersList})

			except Users.DoesNotExist:
				return JsonResponse({'success': False, 'message': 'something went wronng'})



		return JsonResponse({'success': False, 'message': 'some error occured'})


