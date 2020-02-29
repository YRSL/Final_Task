from rest_framework import serializers
from .models import CustomUser, Course, Lecture, Homework, Mark, Comment


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title', 'creator', 'teacher', 'students')


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('topic', 'course', 'creator', 'file')


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ('title', 'lecture', 'task')


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ('value', 'homework')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment', 'creator', 'mark')
