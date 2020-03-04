from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .serializer import (UserRegisterSerializer, UserSerializer, CourseSerializer,
                         CourseDetailSerializer, LectureSerializer, LectureDetailSerializer,
                         HomeworkSerializer, HomeworkDetailSerializer, MarkSerializer, MarkDetailSerializer,
                         CommentSerializer, CommentDetailSerializer, TaskSerializer, TaskDetailSerializer)
from .permissions import IsUserOrReadOnly, IsOwnerOrReadOnly, IsTeacherOrReadOnly, IsStudentOrReadOnly, IsTeacher
from .models import Course, Lecture, Homework, Mark, Comment, Task

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer


class UserView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsUserOrReadOnly)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            data={'token': token.key, 'user_id': user.pk, 'username': user.username},
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class CourseView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsTeacherOrReadOnly, )

    def get_queryset(self):
        user = self.request.user
        if user.role == 0:
            queryset = Course.objects.filter(student=user)
        if user.role == 1:
            queryset = Course.objects.filter(teacher=user)
        return queryset


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, IsTeacherOrReadOnly, )

    def get_queryset(self):
        user = self.request.user
        if user.role == 0:
            queryset = Course.objects.filter(student=user)
        if user.role == 1:
            queryset = Course.objects.filter(teacher=user)
        return queryset


class LectureView(generics.ListCreateAPIView):
    parser_class = (FileUploadParser, )
    serializer_class = LectureSerializer
    permission_classes = (IsAuthenticated, IsTeacherOrReadOnly, )

    def get_queryset(self):
        user = self.request.user
        if user.role == 0:
            queryset = Lecture.objects.filter(course__student=user)
            return queryset
        if user.role == 1:
            queryset = Lecture.objects.filter(course__teacher=user)
            return queryset


class LectureDetailView(generics.RetrieveUpdateDestroyAPIView):
    parser_class = (FileUploadParser, )
    serializer_class = LectureDetailSerializer
    permission_classes = (IsAuthenticated, IsTeacherOrReadOnly, )

    def get_queryset(self):
        user = self.request.user
        if user.role == 1:
            queryset = Lecture.objects.filter(course__student=user)
            return queryset
        if user.role == 2:
            queryset = Lecture.objects.filter(course__teacher=user)
            return queryset


class HomeworkView(generics.ListCreateAPIView):
    serializer_class = HomeworkSerializer
    permission_classes = (IsAuthenticated, IsStudentOrReadOnly, )

    def get_queryset(self):
        user = self.request.user
        if user.role == 0:
            queryset = Homework.objects.filter(author=user)
        if user.role == 1:
            queryset = Homework.objects.filter(task__lecture__course__teacher=user)
        return queryset


class HomeworkDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HomeworkDetailSerializer
    permission_classes = (IsAuthenticated, IsStudentOrReadOnly, IsOwnerOrReadOnly, )

    def get_queryset(self):
        user = self.request.user
        if user.role == 0:
            queryset = Homework.objects.filter(author=user)
        if user.role == 1:
            queryset = Homework.objects.filter(task__lecture__course__teacher=user)
        return queryset


class MarkView(generics.CreateAPIView):
    serializer_class = MarkSerializer
    permission_classes = (IsAuthenticated, IsTeacher, )


class MarkDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MarkDetailSerializer
    permission_classes = (IsAuthenticated, IsTeacherOrReadOnly, IsOwnerOrReadOnly, )

    def get_queryset(self):
        user = self.request.user
        if user.role == 0:
            queryset = Mark.objects.filter(homework__author=user)
        if user.role == 1:
            queryset = Mark.objects.filter(author=user)
        return queryset


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )

    def get_queryset(self):
        user = self.request.user
        if user.role == 1:
            queryset = Comment.objects.filter(grade__homework__author=user)
            return queryset
        if user.role == 2:
            queryset = Comment.objects.filter(grade__author=user)
            return queryset


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )

    def get_queryset(self):
        user = self.request.user
        if user.role == 1:
            queryset = Comment.objects.filter(grade__homework__author=user)
            return queryset
        if user.role == 2:
            queryset = Comment.objects.filter(grade__author=user)
            return queryset

class TaskView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsTeacherOrReadOnly, )

    def get_queryset(self):
        user = self.request.user
        if user.role == 0:
            queryset = Task.objects.filter(lecture__course__student=user)
        if user.role == 1:
            queryset = Task.objects.filter(lecture__course__teacher=user)
        return queryset


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailSerializer
    permission_classes = (IsAuthenticated, IsTeacher, )

    def get_queryset(self):
        user = self.request.user
        if user.role == 0:
            queryset = Task.objects.filter(lecture__course__student=user)
        if user.role == 1:
            queryset = Task.objects.filter(lecture__course__teacher=user)
        return queryset
