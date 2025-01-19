from django import forms
from .models import Category, Equipment
from .widgets import RangeInput

class UserProfileForm(forms.Form):
    age = forms.IntegerField(
        min_value=1,
        max_value=100,
        required=True,
        label="Alter",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    height = forms.IntegerField(
        min_value=1,
        max_value=300,
        required=True,
        label="Größe (cm)",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    weight = forms.IntegerField(
        min_value=1,
        max_value=400,
        required=True,
        label="Gewicht (kg)",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    goal_weight = forms.IntegerField(
        min_value=1,
        max_value=300,
        required=True,
        label="Zielgewicht (kg)",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    training_level = forms.ChoiceField(
        choices=[
            ('beginner', 'Anfänger'),
            ('advanced', 'Fortgeschritten'),
        ],
        required=True,
        label="Trainingslevel",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    training_days = forms.MultipleChoiceField(
        choices=[
            ('montag', 'Montag'),
            ('dienstag', 'Dienstag'),
            ('mittwoch', 'Mittwoch'),
            ('donnerstag', 'Donnerstag'),
            ('freitag', 'Freitag'),
            ('samstag', 'Samstag'),
            ('sonntag', 'Sonntag'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True,
        label="Trainingstage"
    )
    goal = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label="Ziel",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    equipment = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.all(),
        required=False,
        label="Geräte",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    training_duration = forms.ChoiceField(
        choices=[
            ('low', '15 Minuten - 30 Minuten'),
            ('middle', '30 Minuten - 45 Minuten'),
            ('high', '45 Minuten - 60 Minuten'),
        ],
        required=True,
        label="Trainingsdauer",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean_training_days(self):
        training_days = self.cleaned_data.get('training_days')
        if not training_days:
            raise forms.ValidationError("You must select at least one training day.")
        if len(training_days) > 6:
            raise forms.ValidationError("You can select a maximum of 6 training days.")
        return training_days