from rest_framework import serializers
from .models import CustomUser, Course, Lecture, Homework, Mark, Comment


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email')


class UserRegisterSerializer(serializers.ModelSerializer):
    is_student = serializers.BooleanField(default=False)
    is_teacher = serializers.BooleanField(default=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_student', 'is_teacher')

    def save(self):
        student = self.validated_data['is_student']
        teacher = self.validated_data['is_teacher']
        if student:
            user = CustomUser.objects.create_student(email=self.validated_data['email'],
                                                   password=self.validated_data['password'])
            user.save()
            return user

        elif teacher:
            user = CustomUser.objects.create_teacher(email=self.validated_data['email'],
                                                   password=self.validated_data['password'])
            user.save()
            return user


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
