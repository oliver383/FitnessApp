import random
from core.models import UserRecommendation, Exercise
from django.db import models

def generate_user_recommendations(user):
    # Clear old recommendations
    UserRecommendation.objects.filter(user=user).delete()

    user_profile = user.profile
    training_days = user_profile.training_days
    user_goal = user_profile.goal
    user_equipment = user_profile.equipment.all()

    if user_profile.training_duration == 'low':
        exercise_count = user_goal.exercise_count_low
    elif user_profile.training_duration == 'middle':
        exercise_count = user_goal.exercise_count_middle
    else:
        exercise_count = user_goal.exercise_count_high

    # Fetch exercises filtered by goal and equipment
    full_body_exercises = Exercise.objects.filter(
        categories=user_goal
    ).filter(
        models.Q(equipment_needed__in=user_equipment) | models.Q(equipment_needed=None)
    ).distinct()

    upper_body_exercises = Exercise.objects.filter(
        categories=user_goal,
        body_sections__name='oberkörper'
    ).exclude(
        body_sections__name='unterkörper'
    ).filter(
        models.Q(equipment_needed__in=user_equipment) | models.Q(equipment_needed=None)
    ).distinct()

    lower_body_exercises = Exercise.objects.filter(
        categories=user_goal,
        body_sections__name='unterkörper'
    ).exclude(
        body_sections__name='oberkörper'
    ).filter(
        models.Q(equipment_needed__in=user_equipment) | models.Q(equipment_needed=None)
    ).distinct()

    push_exercises = Exercise.objects.filter(
        categories=user_goal,
        pushpull__name='Push'
    ).exclude(
        pushpull__name='Pull'
    ).filter(
        models.Q(equipment_needed__in=user_equipment) | models.Q(equipment_needed=None)
    ).distinct()

    pull_exercises = Exercise.objects.filter(
        categories=user_goal,
        pushpull__name='Pull'
    ).exclude(
        pushpull__name='Push'
    ).filter(
        models.Q(equipment_needed__in=user_equipment) | models.Q(equipment_needed=None)
    ).distinct()

    print(f"Full body exercises: {full_body_exercises}")
    print(f"Upper body exercises: {upper_body_exercises}")
    print(f"Lower body exercises: {lower_body_exercises}")
    print(f"Push body exercises: {push_exercises}")
    print(f"Pull body exercises: {pull_exercises}")

    recommendations = []

    if user_profile.training_level == 'advanced':
        # Advanced logic: Rules based on number of days
        pattern = []
        if len(training_days) == 1:
            pattern = ['Full']
        elif len(training_days) == 2:
            pattern = ['Push', 'Pull']
        elif len(training_days) == 3:
            pattern = ['Push', 'Pull', 'Legs']
        elif len(training_days) == 4:
            pattern = ['Push', 'Pull', 'Push', 'Pull']
        elif len(training_days) == 5:
            pattern = ['Push', 'Pull', 'Legs', 'Push', 'Pull']
        elif len(training_days) == 6:
            pattern = ['Push', 'Pull', 'Legs', 'Push', 'Pull', 'Legs']
        else:
            # TODO: add error
            pass

        for i, day in enumerate(training_days):
            workout_type = pattern[i % len(pattern)]
            if workout_type == 'Push' and push_exercises.exists():
                print(f"Using Push List")
                daily_exercises = random.sample(list(push_exercises),
                                                min(len(push_exercises), exercise_count))
            elif workout_type == 'Pull' and pull_exercises.exists():
                print(f"Using Pull List")
                daily_exercises = random.sample(list(pull_exercises),
                                                min(len(pull_exercises), exercise_count))
            elif workout_type == 'Legs' and lower_body_exercises.exists():
                print(f"Using Lower Body List")
                daily_exercises = random.sample(list(lower_body_exercises),
                                                min(len(lower_body_exercises), exercise_count))
            elif workout_type == 'Full' and full_body_exercises.exists():
                print(f"Using Full Body List")
                daily_exercises = random.sample(list(full_body_exercises),
                                                min(len(full_body_exercises), exercise_count))
            else:
                daily_exercises = []

            # Add recommendations for the day
            for exercise in daily_exercises:
                recommendations.append(UserRecommendation(
                    user=user,
                    exercise=exercise,
                    day_of_week=day
                ))
    else:
        # Beginner logic: Alternating upper and lower body on consecutive days
        use_upper_body = True
        for i, day in enumerate(training_days):
            if has_consecutive_days(training_days, i):
                if use_upper_body and upper_body_exercises.exists():
                    print(f"Using Upper Body List")
                    daily_exercises = random.sample(list(upper_body_exercises),
                                                    min(len(upper_body_exercises), exercise_count))
                    use_upper_body = False
                elif lower_body_exercises.exists():
                    print(f"Using Lower Body List")
                    daily_exercises = random.sample(list(lower_body_exercises),
                                                    min(len(lower_body_exercises), exercise_count))
                    use_upper_body = True
                else:
                    daily_exercises = []  # Fallback
            else:
                print(f"Using Full Body List")
                daily_exercises = random.sample(list(full_body_exercises),
                                                min(len(full_body_exercises),
                                                    exercise_count)) if full_body_exercises.exists() else []


            for exercise in daily_exercises:
                recommendations.append(UserRecommendation(
                    user=user,
                    exercise=exercise,
                    day_of_week=day
                ))


    UserRecommendation.objects.bulk_create(recommendations)


def has_consecutive_days(training_days, current_index):
    days_of_week = ['montag','dienstag','mittwoch','donnerstag','freitag','samstag','sonntag']

    current_day_index = days_of_week.index(training_days[current_index])
    prev_day_index = (current_day_index - 1) % 7
    next_day_index = (current_day_index + 1) % 7
    training_day_indices = [days_of_week.index(day) for day in training_days]

    return prev_day_index in training_day_indices or next_day_index in training_day_indices


