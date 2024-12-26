import random
from core.models import UserRecommendation, Exercise


def generate_user_recommendations(user):
    # Clear old recommendations
    UserRecommendation.objects.filter(user=user).delete()

    # Fetch user preferences
    training_days = user.profile.training_days

    all_exercises = list(Exercise.objects.all())

    recommendations = []
    for day in training_days:
        random_exercise = random.choice(all_exercises)  # Pick a random exercise
        recommendations.append(UserRecommendation(
            user=user,
            exercise=random_exercise,
            day_of_week=day
        ))

    # Save recommendations in bulk
    UserRecommendation.objects.bulk_create(recommendations)


