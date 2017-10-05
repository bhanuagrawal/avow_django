from rest_framework import serializers
from users.models import Users, Follow
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('name', 'username', 'password')


class UserSerializerNew(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('name', 'username', 'password', 'status')



class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('name', 'username')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('name', 'username')

class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('name', 'username', 'status')        



class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'following')


