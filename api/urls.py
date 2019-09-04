from django.urls import path
from .views import current_user, UserList, PostList, PostDetail, CategoryList, SubcategoryList, CategorizedPostList, GetCategoryDetail


# as_view() means that the view is defined as a Class.
urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('posts/', PostList.as_view()),
    path('posts/<int:pk>/', PostDetail.as_view()),
    path('categories/list/', CategoryList.as_view()),
    path('categories/<int:pk>/', GetCategoryDetail.as_view()),
    path('categories/<int:pk>/list/', SubcategoryList.as_view()),
    path('categories/<int:pk>/posts/', CategorizedPostList.as_view()),
]


