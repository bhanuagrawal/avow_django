from django.conf import settings
from users.models import Users, AndroidDevice
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
import copy
import json

def handle_uploaded_file(f):
	with open(settings.MEDIA_ROOT + '/images/' + f.name, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)


def validToken(token, userShouldExit=True):
	try:
		username, device_id = token.split(' ')
		user = Users.objects.get(username=username)
		device = AndroidDevice.objects.get(user=user, device_id=device_id)
		return True
	except Users.DoesNotExist:
		return not userShouldExit
	except AndroidDevice.DoesNotExist:
		return False


def updateToken(loggenInUser, token):
	try:
		username, device_id = token.split(' ')
		return loggenInUser  + " " + device_id
	except Exception as e:
		print e
		return "invalid token"



def verifyToken(*arguments, **keywords):

 	def verifyTokenDecorator(old_function):

	 	def new_function(*args, **kwds):
	 		request = args[0]

	 		if (request.method == 'GET' and keywords['forGetRequest'] ) or (request.method == 'POST' and keywords['forPostRequest'] )  :

				#print request.POST.get(keywords['getUsernamePost'])
		 		try:
		 			token = request.META['HTTP_TOKEN']
		 			print token
		 			if 'getUsernameFromKey' in keywords:
		 				data = json.loads(request.body)
		 				token = updateToken(data[keywords['getUsernameFromKey']], token)
		 			elif 'getUsernameFromParameter' in keywords:
		 				token = updateToken(request.GET.get(keywords['getUsernameFromParameter']), token)
					elif 'getUsernamePost' in keywords:
						print "upload photo", keywords['getUsernamePost']

		 				token = updateToken(request.POST.get(keywords['getUsernamePost']), token)
		 			print token
		 		except Exception as e:
		 			return JsonResponse({'token': 'absent', 'success': False, 'message': 'Authentication Failed'}, status=403)


		 		userShouldExit = keywords.get('userShouldExit', True)
				if not validToken(token, userShouldExit):
					return JsonResponse({'token': 'invalid', 'success': False, 'message': 'Authentication Failed'}, status=403)

			return old_function(*args, **kwds)

		return new_function

	return verifyTokenDecorator