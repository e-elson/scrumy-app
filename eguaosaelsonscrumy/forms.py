from .models import User, ScrumyGoals, GoalStatus
from django.forms import ModelForm, Form
from django import forms

class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

class CreateGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = '__all__'
class MoveGoalForm(Form):
    daily = GoalStatus.objects.get(pk=3)
    weekly = GoalStatus.objects.get(pk=2)
    verify = GoalStatus.objects.get(pk=1)
    done = GoalStatus.objects.get(pk=4)
    # options = ((daily, 'Daily Goal'), (weekly, 'Weekly Goal'),
    #            (verify, 'Verify Goal'), (done, 'Done Goal'))
    options = ((3, daily), (2, weekly),
               (1, verify), (4, done))
    status_name = forms.ChoiceField(choices=options)
