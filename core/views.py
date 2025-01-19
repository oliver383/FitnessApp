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

        user_profile = getattr(request.user, 'profile', None)
        if user_profile is None:
            print(f"No profile redirecting to profile")
            return redirect('profile')

        user_goal = user_profile.goal

        context = {
            'schedule': schedule,
            'goal_name': user_goal.name if user_goal else None,
            'goal_reps': user_goal.reps if user_goal else None,
            'goal_sets': user_goal.sets if user_goal else None,
            'goal_sets_rest': user_goal.sets_rest if user_goal else None,
            'goal_intensity': user_goal.intensity if user_goal else None,
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

    # Get or create the user profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST)

        if form.is_valid():
            # Update profile fields
            user_profile.age = form.cleaned_data['age']
            user_profile.height = form.cleaned_data['height']
            user_profile.weight = form.cleaned_data['weight']
            user_profile.goal_weight = form.cleaned_data['goal_weight']
            user_profile.training_level = form.cleaned_data['training_level']
            user_profile.training_days = form.cleaned_data['training_days']
            user_profile.training_duration = form.cleaned_data['training_duration']
            user_profile.goal = form.cleaned_data.get('goal')
            selected_equipment = form.cleaned_data['equipment']
            user_profile.equipment.set(selected_equipment)

            user_profile.save()

            print(f"Profile saved successfully")

            generate_user_recommendations(request.user)

            print(f"Going home")

            return redirect('home')  # Redirect after saving
        else:
            print("Form errors:", form.errors)
            print("Non-field errors:", form.non_field_errors())
            error_message = "There was an error in the form. Please correct it and try again."
            return render(request, 'profile.html', {'form': form, 'error_message': error_message})
    else:
        # Pre-fill the form with existing profile data
        initial_data = {
            'age': user_profile.age or '',
            'height': user_profile.height or '',
            'weight': user_profile.weight or '',
            'goal_weight': user_profile.goal_weight or '',
            'training_level': user_profile.training_level or '',
            'training_days': user_profile.training_days or '',
            'training_duration': user_profile.training_duration or '',
            'goal': user_profile.goal or None,
            'equipment': user_profile.equipment.all(),  # Pre-fill with selected equipment
        }
        form = UserProfileForm(initial=initial_data)

    return render(request, 'profile.html', {'form': form})

def help_page(request):
    return render(request, 'help.html')
