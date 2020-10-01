from django.contrib import admin
from .models import GoalStatus, ScrumyGoals, ScrumyHistory

# Register your models here.

admin.site.register(ScrumyGoals)
admin.site.register(ScrumyHistory)
admin.site.register(GoalStatus)
