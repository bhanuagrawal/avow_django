from rest_framework import serializers
from feed.models import UserPost, PostReceiver
from users import serializers as user_serializers



class PostSerializer(serializers.HyperlinkedModelSerializer):

	receivers = serializers.SerializerMethodField()
	receivers_count = serializers.SerializerMethodField()
	image = serializers.CharField(source='image_url')

	class Meta:
		model = UserPost
		fields = ('id', 'image', 'time', 'show_info', 'receivers', 'receivers_count')


	def get_receivers(self, post):
		query = "select users.id, username, name from users left join post_receiver on users.id = receiver_id  where post_id = " + str(post.id)
		receivers = PostReceiver.objects.raw(query)
		serializer = user_serializers.UserSearchSerializer(receivers, many=True)
		return serializer.data

	def get_receivers_count(self, post):
		count = len(PostReceiver.objects.filter(post_id=post.id))
		return count
