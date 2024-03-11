from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, LoginForm
from .models import Notification, Patient
from .services.assigned_medications import assigned_medications
from .services.assigned_patients import assigned_patients
from .services.greeting import greeting
from .services.mail_sender import send_interaction_email
from .services.num_patients import worker_patient_count


# Index - Login page
def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
        return render(request, 'index.html', {'form': form})

    return render(request, 'index.html')

# signup page
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



# logout page

def user_logout(request):
    logout(request)
    return redirect('index') #After logout redirect to login (index) page


# Dashboard
@login_required
def dashboard(request):
    user = request.user
    notifications = Notification.objects.filter(user=user, is_read=False)
    current_time = datetime.now()
    greeting_message = greeting()
    patient_count = worker_patient_count(request.user)
    assigned_patient = assigned_patients(request.user)
    assigned_medication = assigned_medications(request.user)



    return render(request, 'dashboard.html', {'current_time': current_time,
                                              'notifications': notifications, 'greeting_message': greeting_message, 'patient_count': patient_count,
                                              'assigned_patient': assigned_patient, 'assigned_medication': assigned_medication})





def task(request):
    assigned_patient = assigned_patients(request.user)
    patient = None
    interaction_completed = None
    note = None
    tasks_completed = []
    current_time = datetime.now()
    greeting_message = greeting()

    if request.method == 'POST':
        # Extracting form data
        patient_id = request.POST.get('name_select')
        interaction_completed = request.POST.get('interaction_completed')
        note = request.POST.get('note')
        tasks_completed = request.POST.getlist('tasks_completed')

        # Sending email
        send_interaction_email(patient_id, interaction_completed, note, tasks_completed)

        # Retrieve patient object
        patient = Patient.objects.get(pk=patient_id)

    return render(request, 'task.html', {'assigned_patient': assigned_patient, 'patient': patient,
                                         'interaction_completed': interaction_completed, 'note': note, 'tasks_completed': tasks_completed, 'current_time': current_time, 'greeting_message': greeting_message})
