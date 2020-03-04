from django.urls import path

from .views import (UserRegistrationView, UserView, UserDetailView,
                    LoginView, LogoutView, CourseView, CourseDetailView, LectureView,
                    LectureDetailView, HomeworkView, HomeworkDetailView, MarkView, MarkDetailView,
                    CommentView, CommentDetailView, TaskView, TaskDetailView)

urlpatterns = [
    path('users/list/', UserView.as_view(), name='users-list'),
    path('users/list/<int:pk>', UserDetailView.as_view(), name='users-detail'),
    path('users/register/', UserRegistrationView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/logout/', LogoutView.as_view(), name='logout'),

    path('courses/', CourseView.as_view(), name='courses'),
    path('courses/<int:pk>', CourseDetailView.as_view(), name='course-detail'),

    path('lectures/', LectureView.as_view(), name='lectures'),
    path('lectures/<int:pk>', LectureDetailView.as_view(), name='lecture-detail'),

    path('homeworks', HomeworkView.as_view(), name='homework'),
    path('homeworks/<int:pk>', HomeworkDetailView.as_view(), name='homework-detail'),

    path('marks', MarkView.as_view(), name='marks'),
    path('marks<int:pk>', MarkDetailView.as_view(), name='grade-detail'),

    path('comments/', CommentView.as_view(), name='comments'),
    path('comments/<int:pk>', CommentDetailView.as_view(), name='comment-detail'),

    path('tasks', TaskView.as_view(), name='tasks'),
    path('tasks/<int:pk>', TaskDetailView.as_view(), name='task-detail')
]