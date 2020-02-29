from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from api.models_managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Course(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ManyToManyField(Teacher, blank=True)
    student = models.ManyToManyField(Student, blank=True)


class Lecture(models.Model):
    course = models.ForeignKey(Course, blank=False, on_delete=models.CASCADE)
    topic = models.CharField(blank=False, max_length=20)
    file = models.FileField()


class Homework(models.Model):
    lecture = models.OneToOneField(Lecture, blank=False, on_delete=models.CASCADE)
    title = models.CharField(blank=False, max_length=20)
    task = models.TextField(lank=False, max_length=400)


class Mark(models.Model):
    mark = models.IntegerField()


class Comment(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    mark = models.ForeignKey(Mark, blank=False, on_delete=models.CASCADE)
    comment = models.CharField(blank=False, max_length=200)
