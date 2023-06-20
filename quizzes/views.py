from django.shortcuts import render, redirect
from .models import Quiz, Question, Rating
import threading, requests
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from random import choice

def make_p():
    l = "abcdefghijklmopqrstuvxyzABDCEFGHIJKLMOPQRSTUVXYZ"
    d = "0123456789"
    p = ""
    for i in range(4):
        p += choice(l)
        p += choice(d)
    return p

def create_user(count):
    for i in range(1, count+1):
        username = f"pupigl{i}"
        password = f"{make_p()}"
        user = User.objects.create_user(
            username=username,
            password=password
        )
        user.save()
        print(username + " | " + password)

class MyThread(threading.Thread):
    def __init__(self, questions, answers, rating, quiz, user):
        self.questions = questions
        self.answers = answers
        self.rating = rating
        self.quiz = quiz
        self.user = user
        threading.Thread.__init__(self)

    def run(self):
        s = 0
        d = {}
        counter = 1
        for question, answer in zip(self.questions, self.answers):
            if question.correct == self.answers[answer][0]:
                print("correct")
                s += 2.5
                d[f"question{counter}"] = {
                    "question": question.question,
                    "correct": question.correct,
                    "answer": self.answers[answer][0],
                    "status": "Accepted"
                }
            else:
                print("incorrect")
                d[f"question{counter}"] = {
                    "question": question.question,
                    "correct": question.correct,
                    "answer": self.answers[answer][0],
                    "status": "Wrong"
                }
            counter += 1
        self.rating.score = s
        self.rating.cases = d
        self.rating.save()
        self.quiz.submiters.add(self.user)
        print(s, self.rating)

def home(request):
    # url = "https://quizme.algorithmshub.uz/api/question/"
    # for i in range(1, 327):
    #     res = requests.get(url + f"{i}/")
    #     q = res.json()["question"]
    #     a1 = res.json()['answer1']
    #     a2 = res.json()['answer2']
    #     a3 = res.json()['answer3']
    #     a4 = res.json()['answer4']
    #     c = res.json()['correct']
    #     Question.objects.create(
    #         question=q,
    #         answer1=a1,
    #         answer2=a2,
    #         answer3=a3,
    #         answer4=a4,
    #         correct=c
    #     )
    #     print(url)
    # create_user(2)
    return render(request, "home.html")

def profile(request, username):
    user = request.user
    quizzes = Quiz.objects.all().filter(users__in=[user.pk])
    return render(request, "profile.html", {"quizzes": quizzes})

def quiz(request, url):
    quiz = Quiz.objects.filter(url=url).first()
    option = quiz.options.all()[1]
    usernotin = True
    if request.user in quiz.submiters.all():
        usernotin = False
    rating = Rating.objects.all().filter(author=request.user).first()
    if rating:
        ...
    else:
        rating = Rating(
            author=request.user,
            quiz=quiz
        )
        rating.save()
    questions = option.questions.all()
    if request.method == "POST":
        data = dict(request.POST)
        data.pop("csrfmiddlewaretoken")
        MyThread(questions, data, rating, quiz, request.user).start()
        return HttpResponseRedirect(reverse("profile", args=[request.user.username]))
    return render(request, 'quiz.html', {"questions": questions, "quiz": quiz, "usernotin": usernotin, "cases": rating.cases, "score": rating.score})

def login_(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("i am")
            return HttpResponseRedirect(reverse('profile', args=[user.get_username()]))
    print("you are")
    return HttpResponseRedirect(reverse("home"))

def results(request, url):
    quiz = Quiz.objects.all().filter(url=url).first()
    ratings = Rating.objects.all().filter(quiz=quiz).order_by("score")
    return render(request, "results.html", {"results": ratings})

