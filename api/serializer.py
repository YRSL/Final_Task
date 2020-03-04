from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

from .models import Course, Lecture, Homework, Mark, Comment, Task

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    UserUniqueValidator = UniqueValidator(queryset=User.objects.all(),
                                          message='Username already exists.')
    EmailUniqueValidator = UniqueValidator(queryset=User.objects.all(),
                                           message='Email already exists.')

    username = serializers.CharField(min_length=5, max_length=15,
                                     validators=[UserUniqueValidator])
    password = serializers.CharField(min_length=5, max_length=25, write_only=True,
                                     required=True, style={'input_type': 'password'})
    email = serializers.EmailField(max_length=50, validators=[EmailUniqueValidator])

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'role', )

    def create(self, validated_data):
        password = validated_data.get('password')
        user = User(
            username=validated_data.get('username'),
            role=validated_data.get('role'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
        )
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.SerializerMethodField('get_role_display')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'role_display', )

    def get_role_display(self, obj):
        return obj.get_role_display()


class CourseSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'author',
                  'student', 'teacher', )


class CourseDetailSerializer(serializers.ModelSerializer):
    lectures = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'author',
                  'student', 'teacher', 'lectures', )
        read_only_fields = ('title', 'author',)


class HomeworkSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Homework
        fields = ('id', 'author', 'file', 'task',)

    def validate_task(self, attrs):
        request = self.context['request']
        tasks = Task.objects.filter(lecture__course__student=request.user)
        if attrs not in tasks:
            msg = 'Not available task'
            raise serializers.ValidationError(msg)
        return attrs


class HomeworkDetailSerializer(serializers.ModelSerializer):
    grade = serializers.SlugRelatedField(read_only=True, slug_field='grade')
    class Meta:
        model = Homework
        fields = ('id', 'author', 'file', 'task', 'grade',)
        read_only_fields = ('task', 'author', )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'grade', )

    def validate_grade(self, attrs):
        request = self.context['request']
        if request.user.role == 0:
            grade = Mark.objects.filter(homework_author=request.user)
        if request.user.role == 1:
            grade = Mark.objects.filter(author=request.user)
        if attrs not in grade:
            msg = 'Not available grade'
            raise serializers.ValidationError(msg)
        return attrs


class CommentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'grade', )
        read_only_fields = ('grade', 'author', )


class MarkSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Mark
        fields = ('id', 'author', 'homework', 'grade', )

    def validate_homework(self, attrs):
        request = self.context['request']
        tasks = Homework.objects.filter(task__lecture__course__teacher=request.user)
        if attrs not in tasks:
            msg = 'Not available task'
            raise serializers.ValidationError(msg)
        return attrs


class MarkDetailSerializer(serializers.ModelSerializer):
    comments = CommentDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Mark
        fields = ('id', 'author', 'homework', 'grade', 'comments', )
        read_only_fields = ('homework', 'author', )


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'author', 'lecture',)

    def validate_lecture(self, attrs):
        request = self.context['request']
        lectures = Lecture.objects.filter(course__teacher=request.user)
        if attrs not in lectures:
            msg = 'Not available lecture'
            raise serializers.ValidationError(msg)
        return attrs


class TaskDetailSerializer(serializers.ModelSerializer):
    homework = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'author', 'lecture', 'homework', )
        read_only_fields = ('lecture', 'author', )


class LectureSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Lecture
        fields = ('id', 'title', 'description', 'author', 'course', 'presentation',)

    def validate_course(self, attrs):
        request = self.context['request']
        courses = Course.objects.filter(teacher=request.user)
        if attrs not in courses:
            msg = 'Not available course'
            raise serializers.ValidationError(msg)
        return attrs


class LectureDetailSerializer(serializers.ModelSerializer):
    tasks = TaskDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Lecture
        fields = ('id', 'title', 'description', 'author', 'course', 'presentation', 'tasks')
        read_only_fields = ('course', 'author', )


