from django.contrib.auth.models import User
from .models import Post, Category
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.utils.timezone import datetime


# Serializer for Getting Current User Information
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


# Serializer for SignUp: Only When the token is required
class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    # password = serializers.CharField(write_only=True)
    # Optional. I choose to specify in the Meta data.

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        user = self.Meta.model(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'token', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class PostSerializer(serializers.ModelSerializer):

    writer = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_writer(self, obj):
        writer = obj.writer_id.username
        return writer

    def get_category(self, obj):
        if obj.category_id == None:
            return None
        category = obj.category_id.title
        return category

    def update(self, post, validated_data):
        post.updated = datetime.now()
        post.title = validated_data.get('title', post.title)
        post.text = validated_data.get('text', post.text)
        post.category_id = validated_data.get('category_id', post.category_id)
        post.save()
        return post

    class Meta:
        model = Post
        fields = ['id', 'created', 'updated', 'writer_id', 'writer', 'category_id', 'category', 'title', 'text']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'parent_category_id']

