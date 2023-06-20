from django.db import models
from django.contrib.auth.models import User


def simple():
    return {}

class Question(models.Model):
    question = models.TextField()

    answer1 = models.TextField()
    answer2 = models.TextField()
    answer3 = models.TextField()
    answer4 = models.TextField()
    correct = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.correct in [self.answer1, self.answer2, self.answer3, self.answer4]:
            return super().save(*args, **kwargs)


class Option(models.Model):
    name = models.CharField(max_length=100)
    questions = models.ManyToManyField(Question, related_name='option_questions')
    created_at = models.DateTimeField(auto_now_add=True)


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    options = models.ManyToManyField(Option, related_name='quiz_options')
    users = models.ManyToManyField(User, related_name="quiz_users")
    submiters = models.ManyToManyField(User, related_name="quiz_submiters")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        url = ""
        url = self.name.lower()
        url = url.replace(" ", "_")
        self.url = url
        return super().save(*args, **kwargs)

# class Pupil(models.Model):
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=10)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     group = models.CharField(max_length=100)

class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    cases = models.JSONField(default=simple)


