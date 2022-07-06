from xml.dom import minicompat
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from app_one.models import *
from django.shortcuts import redirect, render
import bcrypt
from datetime import datetime, timedelta


def index(request):
    return render(request, "Login_Reg.html")


def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            password = request.POST["password"]
            conf_pssword = request.POST["conf_pssword"]
            if(password == conf_pssword):

                salt = bcrypt.gensalt()
                hash = bcrypt.hashpw(password.encode(), salt)
                User.objects.create(
                    first_name=first_name, last_name=last_name, email=email, password=hash.decode())
                messages.success(request, "User registered successfully")
            else:
                messages.error(
                    request, "Password must match the confirmed password")
            return redirect("/")
    return redirect("/register")


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = User.objects.get(email=email)
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                request.session["loggedInUser"] = user.id
                return redirect("/view_wall")

            messages.error(
                request, "incorrect Password")

        except User.DoesNotExist:
            messages.error(
                request, "You do not have an account ,Please Register first !")

        return redirect("/")
    return redirect("/")


def view_wall(request):
    if "loggedInUser" in request.session:
        user = User.objects.get(id=request.session["loggedInUser"])
        context = {
            "user": user,
            "msgs": Message.objects.all(),
            "comments": Comment.objects.all(),
        }
        return render(request, "TheWall.html", context)
    return redirect("/")


def post_message(request):
    if request.method == "POST":
        # create new msg
        user = User.objects.get(id=request.session["loggedInUser"])
        message = request.POST["msg"]
        Message.objects.create(message=message, user=user)
    return redirect("/view_wall")


def post_comment(request):
    if request.method == "POST":
        # create new comment
        user = User.objects.get(id=request.session["loggedInUser"])
        comment = request.POST["comment"]
        msg = Message.objects.get(id=request.POST["messageId"])
        Comment.objects.create(comment=comment, user=user, msg=msg)
    return redirect("/view_wall")

def delete_comment(request, commentId):
    if request.method == "POST":
        Comment.objects.get(id=commentId).delete()
    return redirect("/view_wall")

#delete msg & related comments
def delete_msg(request, msgId):
    if request.method == "POST":
        my_msg = Message.objects.get(id=msgId)
        my_msg.msg.all().delete()
        my_msg.delete()
    return redirect("/view_wall")


def logout(request):
    request.session.flush()
    return redirect("/")
