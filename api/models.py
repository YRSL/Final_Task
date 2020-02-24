from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100)


class Lecture(models.Model):
    name = models.CharField(max_length=100)


class Homework(models.Model):
    name = models.CharField(max_length=100)


class Mark(models.Model):
    name = models.CharField(max_length=100)


class Comment(models.Model):
    name = models.CharField(max_length=100)
