from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

# Define periodicity choices
PERIOD_CHOICES = [
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly')
]

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Name of the habit
    periodicity = models.CharField(max_length=50, choices=PERIOD_CHOICES)  # "daily", "weekly", "monthly"
    created_at = models.DateTimeField(auto_now_add=True)  # When the habit was created

    def __str__(self):
        return self.name

    def complete_habit(self, completion_date=None):
        """Mark the habit as completed for a specific date."""
        if completion_date is None:
            completion_date = date.today()
        CompletedHabit.objects.create(habit=self, completed_on=completion_date)

    def get_streak(self):
        """Calculate the current streak of habit completion."""
        streak_count = 0
        current_date = date.today()
        period_days = {
            'daily': 1,
            'weekly': 7,
            'monthly': 30
        }.get(self.periodicity.lower(), 1)

        while True:
            if self.completed_habits.filter(completed_on=current_date).exists():
                streak_count += 1
            else:
                break
            current_date -= timedelta(days=period_days)

        return streak_count

    def is_habit_broken(self):
        """Check if the habit is broken based on periodicity."""
        last_completion = self.completed_habits.last()
        if last_completion:
            # Check if the last completion date is within the defined period
            return (date.today() - last_completion.completed_on).days > {
                'daily': 1,
                'weekly': 7,
                'monthly': 30
            }.get(self.periodicity.lower(), 1)
        return True  # If no completions exist, the habit is broken

class CompletedHabit(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="completed_habits")
    completed_on = models.DateField()  # Date when the habit was completed

    def __str__(self):
        return f"{self.habit.name} completed on {self.completed_on}"
