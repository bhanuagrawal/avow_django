from django.conf import settings


def handle_uploaded_file(f, filePath):
	with open(filePath,'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)


