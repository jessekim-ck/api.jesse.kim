from django.urls import path
from .views import *


# as_view() means that the view is defined as a Class.
urlpatterns = [
    path('current_user/', current_user),
    path('user/', UserList.as_view()),
    path('post/', PostList.as_view()),
    path('post/<int:pk>/', PostDetail.as_view()),
    path('category/list/', CategoryList.as_view()),
    path('category/<int:pk>/', CategoryDetail.as_view()),
    path('comment/<int:pk>/', CommentList.as_view()),
    path('daylog/', DayLogList.as_view()),
    path('daylog/<int:pk>/', DayLogDetail.as_view()),
]
