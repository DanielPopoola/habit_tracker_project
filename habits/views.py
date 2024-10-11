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