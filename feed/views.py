# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from users.models import Users
from users.models import Follow, AndroidDevice
from users.util import verifyToken
from users.serializers import UserSerializer, UserProfileSerializer


from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm, UploadPhotoForm
from .util import handle_uploaded_file


from models import UserPost, PostReceiver
import users
import time
from django.conf import settings
from .serializers import PostSerializer

import requests
import json

@csrf_exempt
def upload_file(request):
	# if request.method == 'POST':
		
	# 	android_devices_array=[]
	# 	form = UploadFileForm(request.POST, request.FILES)
	# 	if form.is_valid():
	# 		imageName = str(int(time.time())) + request.FILES['file'].name
	# 		filePath = settings.MEDIA_ROOT + '/' + imageName
	# 		url = settings.MEDIA_URL + imageName
	# 		handle_uploaded_file(request.FILES['file'], filePath)
	# 		try:
	# 			user = Users.objects.get(username=request.POST['username'])
	# 			query = "SELECT * FROM `android_devices` where user_id in (select user_id from follow where following_id = "+ str(user.id)+  ") "
	# 			android_devices = AndroidDevice.objects.raw(query)


	# 			for obj in android_devices:
	# 				android_devices_array.append(str(obj.device_id))


	# 			print android_devices_array

	# 			sendNotification(android_devices_array, url);

	# 			post = UserPost(image_url=url, user=user)
	# 			post.save()
	# 			return JsonResponse({'success': True, 'message': 'image uploaded', "url": url, "post_id": post.id})
	# 		except Users.DoesNotExist:
	# 			return JsonResponse({'success': False, 'message': 'user not found'})



	return JsonResponse({'success': False, 'message': 'could not upload image'})


def sendNotification(devices, image_url):
	url = 'https://fcm.googleapis.com/fcm/send'
	body = {
	  
	"data":{  
	   "title":"Avow",
	   "message":"Someone sent you a new photo, check it out",
	   "sound": "default",
	  "url": image_url
	},
	 "registration_ids": devices
	 }
#AAAA8pXjXrs:APA91bEDU3tMPySj_i1I69BtnH0qfpEg8AkHto3tckmNpH24tKGy1K8yPvnyCuXhEbv9Ra2rxXvemLRP1pVKu-j7LXAQxXWXKNVvNY9km5tZQMsDIB0IqdZs_y5Ihb5lrQwHokgMxljo
#AAAA8pXjXrs:APA91bEDU3tMPySj_i1I69BtnH0qfpEg8AkHto3tckmNpH24tKGy1K8yPvnyCuXhEbv9Ra2rxXvemLRP1pVKu-j7LXAQxXWXKNVvNY9km5tZQMsDIB0IqdZs_y5Ihb5lrQwHokgMxljo
#AAAAXIOG_bU:APA91bEW7BNFg_eBcl-0oGbrtWx-4ud3XSz7_BDI6pBN_ZFY4LXfIQi15a5MiKp3lUwJAFP-LmandLiMukcsEDg1GJ-R5fiH4yZhaVnFOeccOjr6Xdl_oDnSLqHZn1fmIh2oXlK2UxyU
	headers = {"Content-Type":"application/json",
			"Authorization": "key=AAAA8pXjXrs:APA91bEDU3tMPySj_i1I69BtnH0qfpEg8AkHto3tckmNpH24tKGy1K8yPvnyCuXhEbv9Ra2rxXvemLRP1pVKu-j7LXAQxXWXKNVvNY9km5tZQMsDIB0IqdZs_y5Ihb5lrQwHokgMxljo"}
	requests.post(url, data=json.dumps(body), headers=headers, verify=False)


@csrf_exempt
def user_feed(request):

	if request.method == 'GET':
		# username = request.GET.get('username')  
		# followers_array=[]
		# following_array=[]
		# try:
		# 	user = Users.objects.get(username=username)
		# 	following = Follow.objects.filter(user=user)

		# 	for obj in following:
		# 		following_array.append(obj.following.id)

		# 	following_array.append(user.id)
		# 	print following_array

		# 	query =  "SELECT * FROM user_post where user_id in (" + ','.join(map(str, following_array)) +  ") and time >= IFNULL((select time  from follow where follow.user_id="+  str(user.id) + " and following_id = user_post.user_id), '2016-01-01') order by user_post.id desc"
		# 	print query
		# 	posts = UserPost.objects.raw(query)

		# except Users.DoesNotExist:
		# 	return JsonResponse({'success': False, 'message': 'user   not found'})

		# postsserializer =  PostSerializer(posts, many=True)
		return JsonResponse({"posts": postsserializer.data})




@csrf_exempt
@verifyToken(forGetRequest=False, forPostRequest=True, getUsernamePost="username")
def upload_photo(request):
	if request.method == 'POST':
		
		android_devices_array=[]
		form = UploadPhotoForm(request.POST, request.FILES)
		if form.is_valid():
			receivers_array = request.POST['receivers'].split(' ')
			notification_receivers = list(receivers_array)
			notification_receivers.remove(request.POST['username'])
			showInfo = False
			try:
				if request.POST['show_info']=="true":
					showInfo = True
				else:
					showInfo = False
			except Exception as e:
				pass
			imageName = str(int(time.time())) + request.FILES['file'].name
			filePath = settings.MEDIA_ROOT + '/' + imageName
			url = settings.MEDIA_URL + imageName
			handle_uploaded_file(request.FILES['file'], filePath)
			try:
				query = "SELECT * FROM `android_devices` left join users on android_devices.user_id = users.id where username in ( " +  ','.join(['"'+receiver+'"' for receiver in notification_receivers])  + " )"
				print query
				android_devices = AndroidDevice.objects.raw(query)


				for obj in android_devices:
					android_devices_array.append(str(obj.device_id))


				print android_devices_array

				sendNotification(android_devices_array, url);

				post = UserPost(image_url=url, show_info=showInfo)
				post.save()

				postReceivers(receivers_array, post);

				return JsonResponse({'success': True, 'message': 'image uploaded', "url": url, "post_id": post.id})
			except Users.DoesNotExist:
				return JsonResponse({'success': False, 'message': 'user not found'})

		return JsonResponse({'success': False, 'message': 'could not upload image'})


def postReceivers(receivers, post):

	for username in receivers:
		try:
			user = Users.objects.get(username=username)
			post_receiver = PostReceiver(post=post, receiver=user)
			post_receiver.save()
		except Users.DoesNotExist:
			return JsonResponse({'success': False, 'message': 'follower not found'})


@csrf_exempt
@verifyToken(forGetRequest=True, forPostRequest=False, getUsernameFromParameter='username')
def user_posts(request):


	if request.method == 'GET':
		username = request.GET.get('username')  
		post_ids=[]
		try:
			user = Users.objects.get(username=username)

			post_receiver_objs = PostReceiver.objects.filter(receiver=user)



			for obj in post_receiver_objs:
				post_ids.append(obj.post_id)

			posts = UserPost.objects.filter(id__in =post_ids).order_by('-id')

		except Users.DoesNotExist:
			return JsonResponse({'success': False, 'message': 'user   not found'})

		postsserializer =  PostSerializer(posts, many=True)

		for post in postsserializer.data:
			post['user_details'] = {"username": "0123456789"}

		return JsonResponse({"posts": postsserializer.data})
		










