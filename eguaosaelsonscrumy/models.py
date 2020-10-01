from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class GoalStatus(models.Model):
    status_name = models.CharField(max_length=15)

    def __str__(self):
        return self.status_name

class ScrumyGoals(models.Model):
    goal_name = models.CharField(max_length=100)
    goal_id = models.AutoField(primary_key=True)
    created_by = models.CharField(max_length=100)
    moved_by = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    goal_status = models.ForeignKey(GoalStatus, on_delete=models.PROTECT)
    user = models.ForeignKey(User, related_name='user_details', on_delete=models.CASCADE)

    def __str__(self):
        return self.goal_name

class ScrumyHistory(models.Model):
    moved_by = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    moved_from = models.CharField(max_length=100)
    moved_to = models.CharField(max_length=100)
    time_of_action = models.DateTimeField()
    goal = models.ForeignKey(ScrumyGoals, on_delete=models.CASCADE)

    def __str__(self):
        return self.created_by
