from django.contrib.auth.models import User
from django.db import models

class Exercise(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class UserRecommendation(models.Model):
    DAYS_OF_WEEK = [
        ('montag', 'Montag'),
        ('dienstag', 'Dienstag'),
        ('mittwoch', 'Mittwoch'),
        ('donnerstag', 'Donnerstag'),
        ('freitag', 'Freitag'),
        ('samstag', 'Samstag'),
        ('sonntag', 'Sonntag'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)  # Match training_days

    def __str__(self):
        return f"{self.user.username} - {self.exercise.name} on {self.day_of_week}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    goal_weight = models.PositiveIntegerField()
    training_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Anfänger'),
            ('advanced', 'Fortgeschritten'),
            ('professional', 'Profi'),
        ]
    )
    training_days = models.JSONField()  # Store days as a list of strings
    goals = models.JSONField()  # Store goals as a list of strings
    equipment = models.JSONField(blank=True, null=True)  # Store equipment as a list of strings
    training_duration = models.CharField(
        max_length=20,
        choices=[
            ('15min', '15 Minuten - 30 Minuten'),
            ('30min', '30 Minuten - 45 Minuten'),
            ('60min', '45 Minuten - 60 Minuten'),
        ]
    )

    def __str__(self):
        return self.user.username
