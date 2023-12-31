# Generated by Django 4.2.6 on 2023-10-27 22:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Incorrectban',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cont', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secquestions0', models.CharField(choices=[('Q0', 'Place you want to visit.'), ('Q1', 'Name of your first pet.'), ('Q2', 'City were you born.'), ('Q3', 'Favorite Movie.'), ('Q4', 'Sport you practice or like the most.'), ('Q5', 'Name of your best childhood friend.'), ('Q6', 'Name of the first book you read.'), ('Q7', 'Food you prefer.'), ('Q8', "Your mother's maiden name."), ('Q9', 'Musical instrument you know how to play or would like to learn.')], default='Q0', max_length=2)),
                ('secanwser0', models.TextField()),
                ('secquestions1', models.CharField(choices=[('Q0', 'Place you want to visit.'), ('Q1', 'Name of your first pet.'), ('Q2', 'City were you born.'), ('Q3', 'Favorite Movie.'), ('Q4', 'Sport you practice or like the most.'), ('Q5', 'Name of your best childhood friend.'), ('Q6', 'Name of the first book you read.'), ('Q7', 'Food you prefer.'), ('Q8', "Your mother's maiden name."), ('Q9', 'Musical instrument you know how to play or would like to learn.')], default='Q0', max_length=2)),
                ('secanwser1', models.TextField()),
                ('secquestions2', models.CharField(choices=[('Q0', 'Place you want to visit.'), ('Q1', 'Name of your first pet.'), ('Q2', 'City were you born.'), ('Q3', 'Favorite Movie.'), ('Q4', 'Sport you practice or like the most.'), ('Q5', 'Name of your best childhood friend.'), ('Q6', 'Name of the first book you read.'), ('Q7', 'Food you prefer.'), ('Q8', "Your mother's maiden name."), ('Q9', 'Musical instrument you know how to play or would like to learn.')], default='Q0', max_length=2)),
                ('secanwser2', models.TextField()),
                ('encrypted', models.BooleanField(default=False)),
                ('From_User', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Entries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=20)),
                ('url', models.URLField(blank=True)),
                ('username', models.TextField(max_length=40)),
                ('password', models.TextField(max_length=100)),
                ('encrypted', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('From_User', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
