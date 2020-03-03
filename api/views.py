from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import CustomUser, Course, Lecture, Homework, Comment

from .serializer import (CustomUserSerializer, CourseSerializer, LectureSerializer, HomeworkSerializer,
                         UserRegisterSerializer, CommentSerializer, MarkSerializer)
from .permissions import IsOwnerOrReadOnly, IsNotYourClassroom, IsTeacherOrReadOnly, IsStudent


@api_view(['POST', ])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully registered a new user'
            data['email'] = user.email
            data['is_student'] = user.is_student
            data['is_teacher'] = user.is_teacher
            token = Token.objects.get(user=user)
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


@permission_classes([IsAdminUser,])
class UserListView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            queryset = Course.objects.filter(students=user)
        elif user.is_teacher:
            queryset = Course.objects.filter(teachers=user)
        elif user.is_superuser:
            queryset = Course.objects.all()
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(teachers=(user,))


@permission_classes([IsAuthenticated, IsTeacherOrReadOnly, IsNotYourClassroom])
class CourseView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


@permission_classes([IsAuthenticated, IsTeacherOrReadOnly])
class LectureListCreateView(generics.ListCreateAPIView):
    serializer_class = LectureSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            queryset = Lecture.objects.filter(
                courses__students=user
            )
        elif user.is_teacher:
            queryset = Lecture.objects.filter(
                courses__teachers=user
            )
        elif self.request.user.is_superuser:
            queryset = Lecture.objects.all()
        return queryset


@permission_classes([IsAuthenticated, IsTeacherOrReadOnly])
class LectureView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()


@permission_classes([IsAuthenticated, IsTeacherOrReadOnly])
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = LectureSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            queryset = Homework.objects.filter(
                lectures__courses__students=user
            )
        elif user.is_teacher:
            queryset = Homework.objects.filter(
                lectures__courses__teachers=user  # lecture
            )
        elif user.is_superuser:
            queryset = Homework.objects.all()

        return queryset


@permission_classes([IsAuthenticated, IsTeacherOrReadOnly])
class TaskView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()


@permission_classes([IsAuthenticated])
class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.filter(comments=self.kwargs['pk'])
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@permission_classes([IsAuthenticated, IsTeacherOrReadOnly])
class CourseLecturesListView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = Lecture.objects.filter(courses=self.kwargs['pk'])
        return queryset


@permission_classes([IsAuthenticated, IsTeacherOrReadOnly])
class LectureTasksListView(generics.ListCreateAPIView):
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        queryset = Homework.objects.filter(lectures=self.kwargs['pk'])
        return queryset


@permission_classes([IsAuthenticated, IsStudent])
class MarkListView(generics.ListAPIView):
    serializer_class = MarkSerializer

    def get_queryset(self):
        queryset = Homework.objects.filter(student=self.request.user)
        return queryset
