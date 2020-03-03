from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from .views import (registration_view, CourseView, CourseListCreateView, UserListView, CourseLecturesListView,
     LectureView, LectureListCreateView, LectureTasksListView, TaskListCreateView, CommentListView, MarkListView)

urlpatterns = [

    path('/auth/', include('rest_framework.urls')),
    path('/register/', registration_view, name='register'),
    path('/login/', obtain_auth_token, name='login'),
    path('/users/', UserListView.as_view()),
    path('/courses/', CourseListCreateView.as_view()),
    path('/courses/<int:pk>/', CourseView.as_view()),
    path('/courses/<int:pk>/lectures', CourseLecturesListView.as_view()),
    path('/lectures/', LectureListCreateView.as_view()),
    path('/lectures/<int:pk>/', LectureView.as_view()),
    path('/lectures/<int:pk>/tasks/', LectureTasksListView.as_view()),
    path('/marks/', MarkListView.as_view()),
    path('/tasks/', TaskListCreateView.as_view()),
    path('/<int:pk>/comments/', CommentListView.as_view())

]