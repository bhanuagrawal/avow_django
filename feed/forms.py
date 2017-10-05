from django import forms

class UploadFileForm(forms.Form):
	username = forms.CharField()
	file = forms.FileField()



class UploadPhotoForm(forms.Form):
	username = forms.CharField()
	file = forms.FileField()
	receivers = forms.CharField()
	