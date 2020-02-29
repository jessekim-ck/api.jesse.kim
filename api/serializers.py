from .models import Post, Category, Comment, DayLog
from django.contrib.auth.models import User
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

    # To use serializer.save() method, we need update() or create() method
    def update(self, post, validated_data):
        post.updated = datetime.now()
        post.title = validated_data.get('title', post.title)
        post.text = validated_data.get('text', post.text)
        post.category_id = validated_data.get('category_id', post.category_id)
        post.save()
        return post

    class Meta:
        model = Post
        fields = [
            'id',
            'created',
            'updated',
            'writer_id',
            'writer',
            'category_id',
            'category',
            'title',
            'text',
            'num_comments',
            'is_private'
        ]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'description',
            'parent_category_id',
            'num_posts',
            'num_total_posts',
        ]


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'created', 'updated', 'post_id', 'nickname', 'text']


class DayLogSerializer(serializers.ModelSerializer):

    def update(self, daylog, validated_data):
        daylog.date = validated_data.get('date', daylog.date)
        daylog.sleep_from = validated_data.get('sleep_from', daylog.sleep_from)
        daylog.sleep_to = validated_data.get('sleep_to', daylog.sleep_to)
        daylog.condition = validated_data.get('condition', daylog.condition)
        daylog.achievement = validated_data.get('achievement', daylog.achievement)
        daylog.memo = validated_data.get('memo', daylog.memo)
        daylog.save()
        return daylog

    class Meta:
        model = DayLog
        fields = "__all__"
