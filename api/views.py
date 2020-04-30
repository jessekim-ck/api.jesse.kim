from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *
from django.db.models import Q


@api_view(['GET'])
def current_user(request):
    user = UserSerializer(request.user)
    return Response(user.data)


class UserList(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        user = UserSerializerWithToken(data=request.data)
        if user.is_valid():
            user.save()
            return Response(user.data, status=status.HTTP_201_CREATED)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


# Actually, the PostList and the PostDetail classes can be merged into one ViewSet.
class PostList(APIView):

    def post(self, request, format=None):
        post = PostSerializer(data=request.data)
        if post.is_valid():
            post.save()
            return Response(post.data, status=status.HTTP_201_CREATED)
        return Response(post.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):

        try:
            # Keyword search or all post lists
            if request.query_params.get("keyword") is not None:
                keyword = request.query_params.get("keyword")
                posts = Post.objects.filter(Q(is_private=False) | Q(writer_id__id=request.user.id)).\
                    filter(Q(title__contains=keyword) | Q(text__contains=keyword)).order_by('-created')
            else:
                # Pagination parameters
                count = int(request.query_params.get("count"))
                from_idx = int(request.query_params.get("from_idx"))

                posts = Post.objects.filter(Q(is_private=False) | Q(writer_id__id=request.user.id)).\
                    filter(id__lt=from_idx).order_by('-created')[:count]
            
            posts = PostSerializer(posts, many=True)
            return Response(posts.data, status=status.HTTP_200_OK)

        except ValueError:
            return Response(
                {"message": "Check the value of 'count' or 'from_idx'"}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class PostDetail(APIView):

    def put(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk)
            post = PostSerializer(post, data=request.data)
            if post.is_valid():
                post.save()
                return Response(post.data, status=status.HTTP_200_OK)
            return Response(post.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"message": "Invalid post id"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk)
            if post.is_private and request.user.is_anonymous:
                return Response({"message": "Private post"}, status=status.HTTP_401_UNAUTHORIZED)
            post = PostSerializer(post)

            comments = Comment.objects.filter(post_id=pk).order_by('created')
            comments = CommentSerializer(comments, many=True)

            return Response(
                {
                    "post": post.data,
                    "comment_list": comments.data
                },
                status=status.HTTP_200_OK
            )
        except Post.DoesNotExist:
            return Response({"message": "Invalid post id"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk)
            post = PostSerializer(post)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({"message": "Invalid post id"}, status=status.HTTP_404_NOT_FOUND)


# Get Parent Category List
class CategoryList(APIView):

    def get(self, request, format=None):
        category_list = Category.objects.filter(parent_category_id=None)
        category_list = CategorySerializer(category_list, many=True)

        post_list = Post.objects.filter(category_id=None).\
            filter(Q(is_private=False) | Q(writer_id__id=request.user.id))
        post_list = PostSerializer(post_list, many=True)

        return Response(
            {
                "category": {"id": None, "title": None, "parent_category_id": None},
                "children_category_list": category_list.data,
                "children_post_list": post_list.data,
            },
            status=status.HTTP_200_OK
        )


# Get Category Information
class CategoryDetail(APIView):

    def get(self, request, pk, format=None):
        category = Category.objects.get(pk=pk)
        category = CategorySerializer(category)

        children_categories = Category.objects.filter(parent_category_id=pk).order_by('-id')
        children_categories = CategorySerializer(children_categories, many=True)

        children_posts = Post.objects.filter(category_id=pk).\
            filter(Q(is_private=False) | Q(writer_id__id=request.user.id)).order_by('-created')
        children_posts = PostSerializer(children_posts, many=True)

        return Response(
            {
                "category": category.data,
                "children_category_list": children_categories.data,
                "children_post_list": children_posts.data,
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
        comment_list = CommentSerializer(comment_list, many=True)
        return Response(comment_list.data, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        comment = CommentSerializer(data=request.data)
        if comment.is_valid():
            comment.save()
            return Response(comment.data, status=status.HTTP_201_CREATED)
        return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)


class DayLogList(APIView):

    def get(self, request, format=None):
        daylogs = DayLog.objects.all().order_by('-date')
        daylogs = DayLogSerializer(daylogs, many=True)
        return Response(daylogs.data, status=status.HTTP_200_OK)

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
            daylog = DayLogSerializer(daylog, data=request.data)
            if daylog.is_valid():
                daylog.save()
                return Response(daylog.data, status=status.HTTP_201_CREATED)
            else:
                return Response(daylog.errors, status=status.HTTP_400_BAD_REQUEST)
        except DayLog.DoesNotExist:
            return Response({"message": "Invalid DayLog id"}, status=status.HTTP_404_NOT_FOUND)
