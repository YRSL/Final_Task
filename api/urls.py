from django.urls import path
from api import views

# from .import views

from .views import UserListView, CourseListView, LectureView, HomeworkView

urlpatterns = [
    path('users/', UserListView.as_view()),
    path('courses/', CourseListView.as_view()),
    path('lectures/', LectureView.as_view()),
    path('homeworks/', HomeworkView.as_view()),

]