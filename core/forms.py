from django import forms
from .widgets import RangeInput

class UserProfileForm(forms.Form):
    age = forms.IntegerField(min_value=10, max_value=100, required=True, label="Alter")
    height = forms.IntegerField(min_value=140, max_value=220, required=True, label="Größe (cm)", widget=RangeInput(attrs={'min': 140, 'max': 220, 'step': 1, 'value': 170}))
    weight = forms.IntegerField(min_value=40, max_value=200, required=True, label="Gewicht (kg)", widget=RangeInput(attrs={'min': 140, 'max': 220, 'step': 1, 'value': 170}) )
    goal_weight = forms.IntegerField(min_value=40, max_value=200, required=True, label="Zielgewicht (kg)")
    training_level = forms.ChoiceField(
        choices=[
            ('beginner', 'Anfänger'),
            ('advanced', 'Fortgeschritten'),
            ('professional', 'Profi'),
        ],
        required=True,
        label="Trainingslevel"
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
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Trainingstage"
    )
    goals = forms.MultipleChoiceField(
        choices=[
            ('abnehmen', 'Abnehmen'),
            ('muskelaufbau', 'Muskelaufbau'),
            ('fit_bleiben', 'Fit bleiben'),
            ('ausdauer', 'Ausdauer'),
            ('flexibilität', 'Flexibilität verbessern'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Ziele"
    )
    equipment = forms.MultipleChoiceField(
        choices=[
            ('keine', 'Keine'),
            ('kurzhantel', 'Kurzhantel'),
            ('widerstandsbänder', 'Widerstandsbänder'),
            ('gym', 'Gym'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Geräte"
    )
    training_duration = forms.ChoiceField(
        choices=[
            ('15min', '15 Minuten - 30 Minuten'),
            ('30min', '30 Minuten - 45 Minuten'),
            ('60min', '45 Minuten - 60 Minuten'),
        ],
        required=True,
        label="Trainingsdauer"
    )
