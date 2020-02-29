from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *


@api_view(['GET'])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Actually, the PostList and the PostDetail classes can be merged into one ViewSet.
class PostList(APIView):

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        if request.user.is_anonymous:
            posts = Post.objects.filter(private=False).order_by('-created')
        else:
            posts = Post.objects.all().order_by('-created')
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PostDetail(APIView):

    def put(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"message": "Invalid post id"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk)
            if post.private and request.user.is_anonymous:
                return Response({"message": "Private post"}, status=status.HTTP_401_UNAUTHORIZED)
            post_serializer = PostSerializer(post)

            comment_list = Comment.objects.filter(post_id=pk).order_by('created')
            comment_serializer = CommentSerializer(comment_list, many=True)

            return Response({
                "post": post_serializer.data,
                "comment_list": comment_serializer.data
            }, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"message": "Invalid post id"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            serializer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({"message": "Invalid post id"}, status=status.HTTP_404_NOT_FOUND)


# Get Parent Category List
class CategoryList(APIView):

    def get(self, request, format=None):
        category_list = Category.objects.filter(parent_category_id=None)
        category_serializer = CategorySerializer(category_list, many=True)

        post_list = Post.objects.filter(category_id=None)
        post_serializer = PostSerializer(post_list, many=True)

        return Response(
            {
                "category": {"id": None, "title": None, "parent_category_id": None},
                "children_category_list": category_serializer.data,
                "children_post_list": post_serializer.data,
            },
            status=status.HTTP_200_OK
        )


# Get Category Information
class CategoryDetail(APIView):

    def get(self, request, pk, format=None):
        category = Category.objects.get(pk=pk)
        category_serializer = CategorySerializer(category)

        children_categories = Category.objects.filter(parent_category_id=pk).order_by('id')
        children_category_serializer = CategorySerializer(children_categories, many=True)

        children_posts = Post.objects.filter(category_id=pk).order_by('-created')
        children_post_serializer = PostSerializer(children_posts, many=True)

        return Response(
            {
                "category": category_serializer.data,
                "children_category_list": children_category_serializer.data,
                "children_post_list": children_post_serializer.data,
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, pk, format=None):
        category = CategorySerializer(data=request.data)
        if category.is_valid():
            category.save()
            return Response(category.data, status=status.HTTP_201_CREATED)
        return Response(category.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentList(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, pk, format=None):
        comment_list = Comment.objects.filter(post_id=pk).order_by('created')
        serializer = CommentSerializer(comment_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        comment = CommentSerializer(data=request.data)
        if comment.is_valid():
            comment.save()
            return Response(comment.data, status=status.HTTP_201_CREATED)
        return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)


class DayLogList(APIView):

    def get(self, request, format=None):
        daylogs = DayLog.objects.all().order_by('-date')
        serializer = DayLogSerializer(daylogs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        daylog = DayLogSerializer(data=request.data)
        if daylog.is_valid():
            daylog.save()
            return Response(daylog.data, status=status.HTTP_201_CREATED)
        else:
            return Response(daylog.errors, status=status.HTTP_400_BAD_REQUEST)


class DayLogDetail(APIView):

    def put(self, request, pk, format=None):
        try:
            daylog = DayLog.objects.get(pk=pk)
            serializer = DayLogSerializer(daylog, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DayLog.DoesNotExist:
            return Response({"message": "Invalid DayLog id"}, status=status.HTTP_404_NOT_FOUND)
