from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import GoalStatus, ScrumyGoals, ScrumyHistory
from django.contrib.auth.models import User, Group
from .forms import SignupForm, CreateGoalForm, MoveGoalForm

# Create your views here.
random_numbers = []
from random import randint
def get_val():
    val = randint(1000, 9999)
    if val not in random_numbers:
        random_numbers.append(val)
        return val
    else:
        get_val()

def index(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            newuser=form.save()
            group = Group.objects.get(name='Developer')
            group.user_set.add(newuser)
            return render(request, 'eguaosaelsonscrumy/success.html')
        else:
            context = {
                'form': form,
            }
            return render(request, 'eguaosaelsonscrumy/index.html', context)
    else:
        form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'eguaosaelsonscrumy/index.html', context)

def move_goal(request,goal_id,user_id):
    if request.method == 'POST':
        form = MoveGoalForm(request.POST)
        status_name = request.POST['status_name']
        goal = ScrumyGoals.objects.get(pk=goal_id)
        current_user = request.user.id
        user_groups = [group.name for group in request.user.groups.all()]
        options = ['Weekly Goal', 'Done Goal', 'Verify Goal', 'Daily Goal']
        ok_to_save = False
        #if status_name in options:
        if 'Developer' in user_groups:
            if status_name != '4' and current_user == user_id:
                ok_to_save = True
        elif 'Quality Assurance' in user_groups:
            if (current_user == user_id) or status_name == '4' and goal.goal_status.status_name == 'Verify Goal':
                ok_to_save = True
        elif 'Admin' in user_groups:
            ok_to_save = True
        elif 'Owner' in user_groups:
            if current_user == user_id:
                ok_to_save = True
        if ok_to_save:
            print(status_name)
            print(type(status_name))
            #status name is set from pk's of each GoalStatus
            goal.goal_status = GoalStatus.objects.get(pk=int(status_name))
            goal.save()
            context = {
                'form': form,
            }
            return render(request, 'eguaosaelsonscrumy/movegoal.html', context)
        else:
            form = MoveGoalForm()
            context = {'error': 'You can\'t perform that action',
                        'form': form}
            return render(request, 'eguaosaelsonscrumy/movegoal.html', context)
    else:
        form = MoveGoalForm()
        context = {
            'form': form,
        }
        return render(request, 'eguaosaelsonscrumy/movegoal.html', context)

def add_goal(request):
    if request.method == 'POST':
        form = CreateGoalForm(request.POST)
        weekly = GoalStatus.objects.get(pk=2)
        current_user = request.user.id
        user_groups = [group.name for group in request.user.groups.all()]
        if 'Developer' in user_groups:
            if form.is_valid():
                pass
            form.cleaned_data
            print("reaching here as a developer")
            print(form.cleaned_data['goal_status'])
            if form.cleaned_data['goal_status'] != weekly:
                print("if clause evaluated")
                form = CreateGoalForm()
                context = {
                    'form': form,
                    'error': 'You are only allowed to create a Weekly Goal',
                }
                return render(request, 'eguaosaelsonscrumy/addgoal.html', context)
            else:
                print("else clause evaluated")
                form.save()
        elif form.is_valid():
            form.save()
        else : print("Invalid Submission")
    else:
        form = CreateGoalForm()
    context = {
        'form': form,
    }
    return render(request, 'eguaosaelsonscrumy/addgoal.html', context)

def home(request):
    eachgoal = ScrumyGoals.objects.filter(goal_name='Keep Learning Django')
    weekly = GoalStatus.objects.get(status_name='Weekly Goal')
    weekly_goals = weekly.scrumygoals_set.all()
    daily = GoalStatus.objects.get(status_name='Daily Goal')
    daily_goals = daily.scrumygoals_set.all()
    verify = GoalStatus.objects.get(status_name='Verify Goal')
    verify_goals = verify.scrumygoals_set.all()
    done = GoalStatus.objects.get(status_name='Done Goal')
    done_goals = done.scrumygoals_set.all()
    context = {'users': User.objects.all(),
               'weekly_goals': weekly_goals,
               'daily_goals': daily_goals,
               'verify_goals': verify_goals,
               'done_goals': done_goals,
               }
    output = ', '.join([e.goal_name for e in eachgoal])
    return render(request, 'eguaosaelsonscrumy/home.html', context)
