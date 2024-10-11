from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Habit

@login_required
def dashboard(request):
    user_habits = Habit.objects.filter(user=request.user)
    context = {
        'habits':user_habits
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
        return redirect('dashboard.html')
    
    return render(request, 'habits/create_habit.html')