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

    # Utility to filter exercises
    def filter_exercises(categories=None, body_section=None, exclude_body_section=None,
                         push_pull=None, exclude_push_pull=None, for_everyone_only=False):
        queryset = Exercise.objects.filter(categories=categories or user_goal)
        if body_section:
            queryset = queryset.filter(body_sections__name=body_section)
        if exclude_body_section:
            queryset = queryset.exclude(body_sections__name=exclude_body_section)
        if push_pull:
            queryset = queryset.filter(pushpull__name=push_pull)
        if exclude_push_pull:
            queryset = queryset.exclude(pushpull__name=exclude_push_pull)
        if for_everyone_only:
            queryset = queryset.filter(is_for_everyone=True)
        return queryset.filter(
            models.Q(equipment_needed__in=user_equipment) | models.Q(equipment_needed=None)
        ).distinct()

    # Define exercise groups with exclusions
    advanced_exercise_groups = {
        'Full': filter_exercises(),
        'Upper': filter_exercises(body_section='oberkörper', exclude_body_section='unterkörper'),
        'Lower': filter_exercises(body_section='unterkörper', exclude_body_section='oberkörper'),
        'Push': filter_exercises(push_pull='Push', exclude_push_pull='Pull'),
        'Pull': filter_exercises(push_pull='Pull', exclude_push_pull='Push'),
        'Push_Upper': filter_exercises(body_section='oberkörper', push_pull='Push', exclude_body_section='unterkörper'),
        'Pull_Upper': filter_exercises(body_section='oberkörper', push_pull='Pull', exclude_body_section='unterkörper'),
    }

    # Define exercise groups for beginners (only Full, Upper, Lower with `is_for_everyone=True`)
    beginner_exercise_groups = {
        'Full': filter_exercises(for_everyone_only=True),
        'Upper': filter_exercises(body_section='oberkörper', exclude_body_section='unterkörper', for_everyone_only=True),
        'Lower': filter_exercises(body_section='unterkörper', exclude_body_section='oberkörper', for_everyone_only=True),
    }

    def add_daily_recommendations(day, workout_type, groups):
        exercises = list(groups.get(workout_type, []))
        print(f"Using {workout_type}")
        daily_exercises = random.sample(exercises, min(len(exercises), exercise_count)) if exercises else []
        for exercise in daily_exercises:
            recommendations.append(UserRecommendation(
                user=user,
                exercise=exercise,
                day_of_week=day
            ))

    recommendations = []

    if user_profile.training_level == 'advanced':
        # Advanced logic: Rules based on number of days
        patterns = {
            1: ['Full'],
            2: ['Push', 'Pull'],
            3: ['Push_Upper', 'Pull_Upper', 'Lower'],
            4: ['Push', 'Pull', 'Push', 'Pull'],
            5: ['Push_Upper', 'Pull_Upper', 'Lower', 'Push_Upper', 'Pull_Upper'],
            6: ['Push_Upper', 'Pull_Upper', 'Lower', 'Push_Upper', 'Pull_Upper', 'Lower'],
        }
        pattern = patterns.get(len(training_days), [])

        for i, day in enumerate(training_days):
            workout_type = pattern[i % len(pattern)]
            add_daily_recommendations(day, workout_type, advanced_exercise_groups)
    else:  # Beginner logic
        use_upper_body = True
        for i, day in enumerate(training_days):
            if has_consecutive_days(training_days, i):
                # Alternate between Upper and Lower body for consecutive days
                workout_type = 'Upper' if use_upper_body else 'Lower'
                use_upper_body = not use_upper_body
            else:
                # Use Full body for non-consecutive days
                workout_type = 'Full'

            # Add recommendations using beginner-specific exercise groups
            add_daily_recommendations(day, workout_type, beginner_exercise_groups)

    # Bulk create recommendations
    UserRecommendation.objects.bulk_create(recommendations)


def has_consecutive_days(training_days, current_index):
    days_of_week = ['montag','dienstag','mittwoch','donnerstag','freitag','samstag','sonntag']

    current_day_index = days_of_week.index(training_days[current_index])
    prev_day_index = (current_day_index - 1) % 7
    next_day_index = (current_day_index + 1) % 7
    training_day_indices = [days_of_week.index(day) for day in training_days]

    return prev_day_index in training_day_indices or next_day_index in training_day_indices


