from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.core.checks.messages import CheckMessage
from django.db import models


class User(AbstractUser):
    pass


class Activity(models.Model):
    location_choices = [
        ("", "Location"),
        ("Central", "Central"),
        ("East", "East"),
        ("West", "West"),
        ("North", "North"),
        ("South", "South")
    ]

    category_choices = [
        ("", "Category"),
        ("Badminton", "Badminton"),
        ("Basketball", "Basketball"),
        ("Football", "Football"),
        ("Golf", "Golf"),
        ("Floorball", "Floorball"),
        ("Swimming", "Swimming"),
        ("Tennis", "Tennis"),
        ("Volleyball", "Volleyball"),
        ("Yoga", "Yoga"),
        ("Cycling", "Cycling"),
        ("Other", "Other")
    ]

    difficulty_choices = [
        ("", "Difficulty"),
        ("Introductory", "Introductory"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced")
    ]

    duration_choices = [
        ("", "Duration"),
        ("-30", "<30min"),
        ("30-1", "30min-1h"),
        ("1-1.5", "1h-1.5h"),
        ("2-2.5", "2h-2.5h"),
        ("2.5-3", "2.5h-3h"),
        ("+3", ">3h")
    ]

    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creator")
    date = models.DateField()
    description = models.CharField(max_length=5000)
    title = models.CharField(max_length=100)
    max_people = models.IntegerField()
    location = models.CharField(choices=location_choices, max_length=64)
    category = models.CharField(choices=category_choices, max_length=64)
    difficulty = models.CharField(choices=difficulty_choices, max_length=64)
    activity_date = models.DateField()
    start_hour = models.TimeField()
    duration = models.CharField(
        blank=True, null=True, max_length=64, choices=duration_choices)
    image = models.CharField(max_length=64, blank=True, null=True)
    about_author = models.CharField(max_length=1000)
    prerequisites = models.CharField(max_length=1000)
    how_to_attend_meeting = models.CharField(max_length=1000)
    attendants = models.ManyToManyField(User, related_name="attendants")

    def __str__(self):
        return f"{self.title} created by {self.creator} on {self.date.strftime('%d %b %Y')}"

    def get_location(self):
        return self.location_choices

    def get_category(self):
        return self.category_choices

    def get_difficulty(self):
        return self.difficulty_choices

    def get_duration(self):
        return self.duration_choices

    def serialize(self):
        return {
            "creator": self.creator.username,
            "date": self.date,
            "description": self.description,
            "title": self.title,
            "max_people": self.max_people,
            "location": self.location,
            "category": self.category,
            "difficulty": self.difficulty,
            "activity_date": self.activity_date,
            "start_hour": self.start_hour,
            "duration": self.duration,
            "image": self.image,
            "prerequisites": self.prerequisites,
            "about_author": self.about_author,
            "how_to_attend_meeting": self.how_to_attend_meeting
        }
