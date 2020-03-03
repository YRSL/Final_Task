from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
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


class Course(models.Model):
    title = models.CharField(max_length=150)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teachers')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='students', blank=True)

    def __str__(self):
        return self.title


class Lecture(models.Model):
    topic = models.CharField(max_length=100, blank=False)
    course = models.ForeignKey(Course, blank=False, on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Author", on_delete=models.CASCADE, blank=False)
    file = models.FileField()

    def __str__(self):
        return self.topic


class Homework(models.Model):
    title = models.CharField(max_length=100, blank=False)
    lecture = models.ForeignKey(Course, blank=False, on_delete=models.CASCADE)
    task = models.TextField(max_length=400, blank=False)

    def __str__(self):
        return self.title


class Mark(models.Model):
    value = models.PositiveIntegerField()
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)

    def __str__(self):
        return self.value


class Comment(models.Model):
    comment = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                verbose_name="Author of this comment",
                                blank=False,
                                on_delete=models.CASCADE)
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
