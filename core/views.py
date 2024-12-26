from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserProfileForm
from .models import UserProfile, UserRecommendation
from .recommend import generate_user_recommendations


def home(request):
    if request.user.is_authenticated:
        # Fetch user recommendations, grouped by day of the week
        recommendations = UserRecommendation.objects.filter(user=request.user).order_by('day_of_week')

        # Organize recommendations by day of the week
        schedule = {}
        for day, label in UserRecommendation.DAYS_OF_WEEK:
            schedule[day] = recommendations.filter(day_of_week=day)

        context = {
            'schedule': schedule,
        }
    else:
        context = {}

    return render(request, 'home.html', context)

def update_recommendations_view(request):
    if request.user.is_authenticated:
        generate_user_recommendations(request.user)
        return redirect('home')
    return redirect('login')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    print(f"Found profile: {user_profile.age}")

    print(f"method {request.method}")
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            # Update the profile
            user_profile.age = form.cleaned_data['age']
            user_profile.height = form.cleaned_data['height']
            user_profile.weight = form.cleaned_data['weight']
            user_profile.goal_weight = form.cleaned_data['goal_weight']
            user_profile.training_level = form.cleaned_data['training_level']
            user_profile.training_days = form.cleaned_data['training_days']
            user_profile.goals = form.cleaned_data['goals']
            user_profile.equipment = form.cleaned_data['equipment']
            user_profile.training_duration = form.cleaned_data['training_duration']
            user_profile.save()
            return redirect('home')  # Redirect after saving
    else:
        # Pre-fill the form with existing profile data
        print("here")
        initial_data = {
            'age': user_profile.age,
            'height': user_profile.height,
            'weight': user_profile.weight,
            'goal_weight': user_profile.goal_weight,
            'training_level': user_profile.training_level,
            'training_days': user_profile.training_days,
            'goals': user_profile.goals,
            'equipment': user_profile.equipment,
            'training_duration': user_profile.training_duration,
        }
        print(initial_data)
        form = UserProfileForm(initial=initial_data)

    return render(request, 'profile.html', {'form': form})
