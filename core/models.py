from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    reps = models.CharField(max_length=20, default="1")
    sets = models.CharField(max_length=20, default="1")
    sets_rest = models.CharField(max_length=20, default="1")
    intensity = models.CharField(max_length=20, default="1")

    exercise_count_low = models.PositiveIntegerField(default=1)
    exercise_count_middle = models.PositiveIntegerField(default=1)
    exercise_count_high = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class BodySection(models.Model):
    name = models.CharField(
        max_length=11,
        choices=[
            ('oberkörper', 'Oberkörper'),
            ('unterkörper', 'Unterkörper'),
        ],
        unique=True
    )

    def __str__(self):
        return self.get_name_display()

class Muscle(models.Model):
    name = models.CharField(
        max_length=19,
        choices=[
            ('Shoulders Anterior', 'Schultern Anterior'),
            ('Shoulders Posterior', 'Schultern Posterior'),
            ('Triceps', 'Trizeps'),
            ('Biceps', 'Bizeps'),
            ('Chest', 'Brust'),
            ('Back', 'Rücken'),
            ('Core', 'Core'),
            ('Forearm', 'Unterarm'),
            ('Neck', 'Nacken'),
            ('Glutes', 'Gesässmuskel'),
            ('Calves', 'Waden'),
            ('Quadriceps', 'Quadrizeps'),
            ('Hamstrings', 'Hamstrings'),
        ],
        unique=True
    )

    def __str__(self):
        return self.get_name_display()

class Pushpull(models.Model):
    name = models.CharField(
        max_length=7,
        choices=[
            ('Push', 'Push'),
            ('Pull', 'Pull'),
            ('Neither','Neither'),

        ],
        unique=True
    )

    def __str__(self):
        return self.get_name_display()

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    is_for_everyone = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, related_name="exercises")
    equipment_needed = models.ManyToManyField(Equipment, blank=True)
    body_sections = models.ManyToManyField(
        'BodySection',
        related_name='exercises',
        blank=True
    )
    muscles = models.ManyToManyField(
        'Muscle',
        related_name='exercises',
        blank=True
    )
    pushpull = models.ManyToManyField(
        'Pushpull',
        related_name='exercises',
        blank=True
    )
    url = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Optional: Add a link to a video or tutorial for this exercise."
    )

    def __str__(self):
        return self.name

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
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)

    def __str__(self):
        return f"{self.user.username} - {self.exercise.name} on {self.day_of_week}"

class UserProfile(models.Model):
    TRAINING_LEVEL_CHOICES = [
        ('beginner', 'Anfänger'),
        ('advanced', 'Fortgeschritten'),
    ]

    TRAINING_DURATION_CHOICES = [
        ('low', '15 Minuten - 30 Minuten'),
        ('middle', '30 Minuten - 45 Minuten'),
        ('high', '45 Minuten - 60 Minuten'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField(default=18)
    height = models.PositiveIntegerField(default=150)
    weight = models.PositiveIntegerField(default=70)
    goal_weight = models.PositiveIntegerField(default=70)
    training_level = models.CharField(max_length=20, choices=TRAINING_LEVEL_CHOICES, default='beginner')
    training_days = models.JSONField(default=list)  # Store days as a list of strings
    goal = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="user_goal", null=True, blank=True)
    equipment = models.ManyToManyField(Equipment, blank=True)  # Link to Equipment model
    training_duration = models.CharField(max_length=20, choices=TRAINING_DURATION_CHOICES, default='middle')

    def __str__(self):
        return self.user.username

    def clean(self):
        """
        Custom validation to ensure at least one training day is selected.
        """
        super().clean()

        print(f"checking {self.training_days}")

        # Ensure at least one training day is selected
        if not self.training_days or not isinstance(self.training_days, list) or len(self.training_days) == 0:
            raise ValidationError({
                'training_days': "You must select at least one training day."
            })

        # Validate maximum training days (optional, if required)
        if len(self.training_days) > 6:
            raise ValidationError({
                'training_days': "You can select a maximum of 6 training days."
            })