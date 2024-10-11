from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Habit
from .forms import MarkCompletedForm

@login_required
def dashboard(request):

    habits = Habit.objects.filter(user=request.user)

    # Handle form submission for marking habit as completed
    if request.method == 'POST':
        form = MarkCompletedForm(request.POST)
        if form.is_valid():
            habit_id = form.cleaned_data['habit_id']
            try:
                habit = Habit.objects.get(id=habit_id, user=request.user)
                habit.complete_habit()  # Mark the habit as completed
                messages.success(request, f'Habit "{habit.name}" marked as completed.')
            except Habit.DoesNotExist:
                messages.error(request, 'Habit not found.')
        return redirect('dashboard')
    # Calculate streaks for each habit
    habits_with_streaks = [{'habit': habit, 'streak': habit.get_streak()} for habit in habits]
    
    context = {
        'habits_with_streaks': habits_with_streaks,
        'form': MarkCompletedForm(),  # Include the form in the context
    }
    return render(request, 'habits/dashboard.html', context)


@login_required
def create_habit(request):
    if request.method == 'POST':
        name = request.POST['name']
        periodicity = request.POST['periodicity']
        start_date = request.POST['start_date']

        habit = Habit.objects.create(
            user = request.user,
            name=name,
            periodicity=periodicity,
            created_at=start_date
        )
        return redirect('dashboard')
    return render(request, 'habits/create_habit.html')

@login_required
def delete_habit(request, habit_id):
    try:
        habit = Habit.objects.get(id=habit_id, user=request.user)
        habit.delete()
        messages.success(request, f'Habit "{habit.name}" has been deleted.')
    except Habit.DoesNotExist:
        messages.error(request, 'Habit not found.')
    return redirect('dashboard')


@login_required
def habit_analysis(request):
    # Get all currently tracked habits for the user
    all_habits = Habit.objects.filter(user=request.user)
    
    # Get habits grouped by periodicity
    habits_by_periodicity = {}
    for habit in all_habits:
        if habit.periodicity not in habits_by_periodicity:
            habits_by_periodicity[habit.periodicity] = []
        habits_by_periodicity[habit.periodicity].append(habit)

    # Calculate longest run streak for all defined habits
    longest_streak = max([habit.get_streak() for habit in all_habits], default=0)

    # Calculate longest run streak for each habit
    longest_streaks_per_habit = {habit.name: habit.get_streak() for habit in all_habits}

    context = {
        'all_habits': all_habits,
        'habits_by_periodicity': habits_by_periodicity,
        'longest_streak': longest_streak,
        'longest_streaks_per_habit': longest_streaks_per_habit,
    }
    
    return render(request, 'habits/habit_analysis.html', context)
