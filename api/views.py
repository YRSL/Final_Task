from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import CustomUser, Course, Lecture, Homework
from .serializer import CustomUserSerializer, CourseSerializer, LectureSerializer, HomeworkSerializer
from .permissions import IsOwnerOrReadOnly, IsTeacherOrReadOnly


@permission_classes([IsAdminUser,])
class UserListView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
class CourseListView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


@permission_classes([IsAuthenticated, IsTeacherOrReadOnly])
class LectureView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()


@permission_classes([IsAuthenticated, IsTeacherOrReadOnly])
class HomeworkView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()




