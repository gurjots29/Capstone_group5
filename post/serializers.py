from rest_framework import serializers
from post.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'user', 'file']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'created_at', 'post')

    def create(self, validated_data):
        post_id = self.context['request'].data.get('post_id')
        if post_id:
            post = Post.objects.get(id=post_id)
            validated_data['post'] = post
        return super(CommentSerializer, self).create(validated_data)