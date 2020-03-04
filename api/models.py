from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    teacher = 0
    student = 1

    ROLE_CHOICES = (
        (0, 'Student'),
        (1, 'Teacher'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)

    def __str__(self):
        return '{} {} ({})'.format(self.first_name, self.last_name, self.id)


class Course(models.Model):
    title = models.CharField(db_index=True, unique=True, max_length=64)
    description = models.TextField(max_length=256)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    student = models.ManyToManyField(User, blank=True, related_name='students',
                                     limit_choices_to={'role': 0})
    teacher = models.ManyToManyField(User, blank=True, related_name='teachers',
                                     limit_choices_to={'role': 1})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Lecture(models.Model):
    title = models.CharField(db_index=True, unique=True, max_length=64)
    description = models.TextField(max_length=256)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lectures')
    presentation = models.FileField(upload_to='presentation/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return '{}, ({})'.format(self.title, self.course.title)

    class Meta:
        ordering = ['title']


class Task(models.Model):
    title = models.CharField(db_index=True, unique=True, max_length=64)
    description = models.TextField(max_length=256)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return '{} ({})'.format(self.title, self.lecture.title)

    class Meta:
        ordering = ['title']


class Homework(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homework')
    file = models.FileField(blank=True, null=True, upload_to='homework/%Y/%m/%d')
    task = models.ForeignKey(Task, on_delete=models.SET_NULL,
                             blank=True, null=True, related_name='homework')

    def __str__(self):
        return '{} {}'.format(self.author.first_name, self.author.last_name)


class Mark(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')
    homework = models.OneToOneField(Homework, on_delete=models.CASCADE, related_name='grade')
    grade = models.IntegerField()

    def __str__(self):
        return '{} ({})'.format(self.grade, self.author.first_name)


class Comment(models.Model):
    grade = models.ForeignKey(Mark, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=1024)

    def __str__(self):
        return '{} {}'.format(self.author.first_name, self.author.last_name)
