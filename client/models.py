from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.


class Questions(models.Model):
    secquestions0 = models.CharField(
        max_length=2,
        choices=[
            ("Q0", "Place you want to visit."),
            ("Q1", "Name of your first pet."),
            ("Q2", "City were you born."),
            ("Q3", "Favorite Movie."),
            ("Q4", "Sport you practice or like the most."),
            ("Q5", "Name of your best childhood friend."),
            ("Q6", "Name of the first book you read."),
            ("Q7", "Food you prefer."),
            ("Q8", "Your mother's maiden name."),
            ("Q9", "Musical instrument you know how to play or would like to learn."),
        ],
        default="Q0",
    )

    secanwser0 = models.TextField(null=False)

    secquestions1 = models.CharField(
        max_length=2,
        choices=[
            ("Q0", "Place you want to visit."),
            ("Q1", "Name of your first pet."),
            ("Q2", "City were you born."),
            ("Q3", "Favorite Movie."),
            ("Q4", "Sport you practice or like the most."),
            ("Q5", "Name of your best childhood friend."),
            ("Q6", "Name of the first book you read."),
            ("Q7", "Food you prefer."),
            ("Q8", "Your mother's maiden name."),
            ("Q9", "Musical instrument you know how to play or would like to learn."),
        ],
        default="Q0",
    )

    secanwser1 = models.TextField(null=False, verbose_name="Anwser 2")

    secquestions2 = models.CharField(
        max_length=2,
        choices=[
            ("Q0", "Place you want to visit."),
            ("Q1", "Name of your first pet."),
            ("Q2", "City were you born."),
            ("Q3", "Favorite Movie."),
            ("Q4", "Sport you practice or like the most."),
            ("Q5", "Name of your best childhood friend."),
            ("Q6", "Name of the first book you read."),
            ("Q7", "Food you prefer."),
            ("Q8", "Your mother's maiden name."),
            ("Q9", "Musical instrument you know how to play or would like to learn."),
        ],
        default="Q0",
    )
    secanwser2 = models.TextField(null=False, verbose_name="Anwser 3")

    From_User = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)

    encrypted = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return f"{User}"

class UploadFileForm(forms.Form):
    file = forms.FileField()