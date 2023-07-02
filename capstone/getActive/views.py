# imports
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import query
from django.forms.forms import Form
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django import forms
import datetime
import json
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from .models import User, Activity


class newActivityForm(forms.Form):
    obj = Activity()
    difficulty_choices = obj.get_difficulty()
    duration_choices = obj.get_duration()
    category_choices = obj.get_category()
    location_choices = obj.get_location()

    title = forms.CharField(label="", widget=forms.TextInput(attrs={
                            'autocomplete': 'off', "autofocus": True, "placeholder": "Title of Activity", "id": "new_activity_title_form"}), max_length=50)
    text = forms.CharField(label="Description", widget=forms.Textarea(
        attrs={'autocomplete': 'off', "placeholder": "Description", "id": "new_activity_descr"}))
    max_people = forms.IntegerField(widget=forms.NumberInput(
        attrs={"placeholder": "Max. participants"}))
    activity_date = forms.DateField(
        label="Activity date", widget=forms.DateInput(attrs={"type": "date"}))
    start_hour = forms.TimeField(
        label="Start time", widget=forms.TimeInput(attrs={"type": "time"}))

    difficulty = forms.CharField(
        widget=forms.Select(choices=difficulty_choices))
    location = forms.CharField(
        label="Location", widget=forms.Select(choices=location_choices))
    category = forms.CharField(
        label="Activity", widget=forms.Select(choices=category_choices))
    duration = forms.CharField(widget=forms.Select(choices=duration_choices))

    about_author = forms.CharField(label="About Organiser", widget=forms.Textarea(
        attrs={'autocomplete': 'off', "placeholder": "Give attendees some information about the organiser", "id": "new_activity_aboutAuther"}))
    prerequisites = forms.CharField(label="Pre-requisites", widget=forms.Textarea(
        attrs={'autocomplete': 'off', "placeholder": "Tell attendees if there are any pre-requisites (things people should already know before the activity)", "id": "new_activity_prerequisites"}))
    how_how_to_attend_meeting = forms.CharField(label="How to join the activity", widget=forms.Textarea(
        attrs={'autocomplete': 'off', "placeholder": "Explain to people how to join the activity (only visible to the enrolled). Add any links to online video-conferencing apps, your contact information, and other relevant info", "id": "new_activity_prerequisites"}))


def activities(request):
    return render(request, "getActive/activities.html")


def activities(request):
    if request.method == "GET":
        return render(request, "getActive/activities.html", {
            "form": searchActivityForm()
        })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("activities"))
        else:
            return render(request, "getActive/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "getActive/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("activities"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "getActive/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "getActive/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("activities"))
    else:
        return render(request, "getActive/register.html")


@csrf_exempt
def new_activity(request, type):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if type == 1:
        if request.method == "POST":
            form = newActivityForm(request.POST)

            if form.is_valid():
                title = form.cleaned_data["title"]
                text = form.cleaned_data["text"]
                max_people = form.cleaned_data["max_people"]
                activity_date = form.cleaned_data["activity_date"]
                start_hour = form.cleaned_data["start_hour"]
                duration = form.cleaned_data["duration"]
                location = form.cleaned_data["location"]
                category = form.cleaned_data["category"]
                difficulty = form.cleaned_data["difficulty"]
                about_author = form.cleaned_data["about_author"]
                prerequisites = form.cleaned_data["prerequisites"]
                how_how_to_attend_meeting = form.cleaned_data["how_how_to_attend_meeting"]

            else:
                return render(request, "getActive/new_activity.html", {
                    "form": form
                })
            try:
                img = request.FILES["img"]
                fs = FileSystemStorage()
                name = fs.save(img.name, img)
                url = fs.url(name)

            except KeyError:
                url = None

            user = request.user
            date = datetime.datetime.now()

            Activity(creator=user, date=date, description=text, title=title, image=url,
                     max_people=max_people, activity_date=activity_date, start_hour=start_hour,
                     duration=duration, location=location, category=category, difficulty=difficulty, prerequisites=prerequisites,
                     about_author=about_author, how_to_attend_meeting=how_how_to_attend_meeting).save()
            return HttpResponseRedirect(reverse("activities"))

        else:
            try:
                obj = Activity.objects.filter(
                    creator=request.user).order_by("-date")[0]
                if obj.date == datetime.date.today():
                    return render(request, "getActive/new_activity.html", {
                        "error": "You can only create one activity each day"
                    })

            except:
                pass

            return render(request, "getActive/new_activity.html", {
                "form": newActivityForm()
            })

    else:
        if request.method == "PUT":
            data = json.loads(request.body)
            try:
                obj = Activity.objects.filter(
                    creator=request.user).order_by("-date")[0]
            except:
                return JsonResponse({"error": "forbidden"})

        elif request.method == "POST":
            obj = Activity.objects.filter(
                creator=request.user).order_by("-date")[0]
            return JsonResponse({"len1": False, "len2": False})

        else:
            return render(request, "getActive/new_activity.html", {
                "form": newActivityForm()
            })


@csrf_exempt
def filter_activities(request, page):
    data = json.loads(request.body)

    if data["type"] == "all":
        final = Activity.objects.all()

    elif data["type"] == "query":
        final = get_by_title(data["query"])
        if activities == "ERROR":
            return JsonResponse({"ERROR": "No matching activity"})

    elif data["type"] == "filter":
        all_activities = list(Activity.objects.all())
        filtered_activities_dl = list(all_activities)

        for activity in all_activities:
            if activity.difficulty != data["difficulty"] and data["difficulty"] != "":
                filtered_activities_dl.remove(activity)

            if activity.location != data["location"] and data["location"] != "":
                filtered_activities_dl.remove(activity.location)

            if activity.category != data["category"] and data["category"] != "":
                try:
                    filtered_activities_dl.remove(activity)
                except ValueError:
                    pass

        filtered_activities_dltaa = list(filtered_activities_dl)
        filtered_activities_dltad = list(filtered_activities_dltaa)
        for element in filtered_activities_dltad:
            if data["date"] == "Today":
                if str(element.date) != datetime.datetime.now().strftime("%Y-%m-%d"):
                    filtered_activities_dltad.remove(element)

            elif data["date"] == "Tomorrow":
                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                if str(element.date) != tomorrow.strftime("%Y-%m-%d"):
                    filtered_activities_dltad.remove(element)

            elif data["date"] == "Next 7 days":
                next_week = datetime.datetime.now() + datetime.timedelta(days=7)
                if str(element.date) > next_week.strftime("%Y-%m-%d") or str(element.date) <= datetime.datetime.now().strftime("%Y-%m-%d"):
                    filtered_activities_dltad.remove(element)

            elif data["date"] == "Next 30 days":
                new_month = datetime.datetime.now() + datetime.timedelta(days=30)
                if str(element.date) > new_month.strftime("%Y-%m-%d") or str(element.date) <= datetime.datetime.now().strftime("%Y-%m-%d"):
                    filtered_activities_dltad.remove(element)

            elif data["date"] == "Later":
                new_month = datetime.datetime.now() + datetime.timedelta(days=30)
                if str(element.date) < new_month.strftime("%Y-%m-%d"):
                    filtered_activities_dltad.remove(element)

        final_filtered_activities = list(filtered_activities_dltad)
        for element in filtered_activities_dltad:
            if data["max_people"] == "0-10":
                if element.max_people < 0 or element.max_people > 10:
                    final_filtered_activities.remove(element)

            elif data["max_people"] == "10-50":
                if element.max_people < 10 or element.max_people > 50:
                    final_filtered_activities.remove(element)

            elif data["max_people"] == "50-100":
                if element.max_people < 50 or element.max_people > 100:
                    final_filtered_activities.remove(element)

            elif data["max_people"] == "100-500":
                if element.max_people < 100 or element.max_people > 500:
                    final_filtered_activities.remove(element)

            elif data["max_people"] == "+500":
                if element.max_people < 500:
                    final_filtered_activities.remove(element)

        query_activities = get_by_title(data["query"])
        if query_activities == "ERROR":
            return JsonResponse({"ERROR": "No matching activities"})

        final = list(final_filtered_activities)
        for e in final_filtered_activities:
            if e not in query_activities:
                final.remove(e)

    results = []
    for e in final:
        if e.serialize() not in results:
            results.append(e.serialize())

    results.reverse()

    return JsonResponse(results, safe=False)


def get_by_title(query):
    try:
        activities = list(Activity.objects.filter(title__contains=query))
    except Activity.DoesNotExist:
        return "ERROR"

    activities_descr = list(
        Activity.objects.filter(description__contains=query))
    activities.extend(activities_descr)

    return activities

class searchActivityForm(forms.Form):
    obj = Activity()
    difficulty_choices = obj.get_difficulty()
    category_choices = obj.get_category()
    location_choices = obj.get_location()

    date_choices = [("", "Date"), ("Today", "Today"), ("Tomorrow", "Tomorrow"), (
        "Next 7 days", "Next 7 days"), ("Next 30 days", "Next 30 days"), ("Later", "Later")]
    max_people_choices = [("", "Max people"), ("0-10", "0-10"), ("10-50", "10-50"),
                          ("50-100", "50-100"), ("100-500", "100-500"), ("+500", "+500")]
    difficulty = forms.CharField(label="", widget=forms.Select(choices=difficulty_choices, attrs={
                                 "id": "search_difficulty", "class": "search_filters form_activity_fields"}), required=False)
    location = forms.CharField(label="", widget=forms.Select(choices=location_choices, attrs={
                               "id": "search_location", "class": "search_filters form_activity_fields"}), required=False)
    category = forms.CharField(label="", widget=forms.Select(choices=category_choices, attrs={
                               "id": "search_category", "class": "search_filters form_activity_fields"}), required=False)
    date = forms.CharField(label="", widget=forms.Select(choices=date_choices, attrs={
                           "id": "search_date", "class": "search_filters form_activity_fields"}), required=False)
    max_people = forms.CharField(label="", widget=forms.Select(choices=max_people_choices, attrs={
                                 "id": "search_maxPeople", "class": "search_filters form_activity_fields"}), required=False)


def activity(request, title):
    if request.method == "GET":
        try:
            activity = Activity.objects.get(title=title)
            data = [activity.serialize()]

        except Activity.DoesNotExist:
            data = "error"

        return render(request, "getActive/activity.html", {
            "data": data[0],
            "isAttendant": request.user in activity.attendants.all()
        })


@csrf_exempt
def enroll(request, title):
    if request.method == "POST":
        activity = Activity.objects.get(title=title)
        user = request.user

        if user in activity.attendants.all():
            activity.attendants.remove(user)
            return JsonResponse({"enrolled": False})
        else:
            activity.attendants.add(user)
            return JsonResponse({"enrolled": True})


def my_activities(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "getActive/my_activities.html")


@csrf_exempt
def get_enrrolled_activities(request):
    user = request.user
    activities = Activity.objects.all()

    enrolled_activities = []
    for activity in activities:
        if user in activity.attendants.all():
            enrolled_activities.append(activity.serialize())

    return JsonResponse(enrolled_activities, safe=False)
