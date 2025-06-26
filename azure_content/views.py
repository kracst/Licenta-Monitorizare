from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import CreateUserForm

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
        
    return render(request, 'azure_content/register.html',{'form':form})

def loginPage(request):
    form = AuthenticationForm(request, data=request.POST or None)  # Use built-in form

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()  # Get authenticated user
            login(request, user)  # Log the user in
            return redirect('dashboard')  # Redirect to dashboard
        else:
            messages.info(request, "Username OR Password is incorect")

    return render(request, 'azure_content/login.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('home')

class HomeView(ListView):
    context_object_name = 'project_list'
    model = Project
    template_name = "azure_content/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch the latest 10 sensor data
        context['sensor_data'] = SensorData.objects.all().order_by('-timestamp')[:10]
        return context
    
@login_required(login_url='login')
def about(request):
    # Get the latest sensor data
    sensor_data = SensorData.objects.order_by('-timestamp')[:10]  # Fetch the last 10 readings

    return render(request, 'azure_content/about.html', {'sensor_data': sensor_data})

class ProjectCreateView(CreateView):
    model = Project
    fields = ['name', 'description']
    template_name = "azure_content/create.html"
    success_url ="/"

class ProjectEditView(UpdateView):
    model = Project
    fields = ['name','description']
    template_name = "azure_content/create.html"
    success_url ="/"

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "azure_content/delete.html"
    fields = ['name']
    success_url ="/"

@login_required(login_url='login')
def dashboard(request):
    # Get the latest sensor data
    sensor_data = SensorData.objects.order_by('-timestamp')[:10]  # Fetch the last 10 readings

    return render(request, 'azure_content/dashboard.html', {'sensor_data': sensor_data})

@csrf_exempt  # Disable CSRF for simplicity (only for testing!)
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received JSON:", data)  # Debugging line

            temperature = data.get('temperature')
            humidity = data.get('humidity')

            if temperature is not None and humidity is not None:
                SensorData.objects.create(temperature=temperature, humidity=humidity, timestamp=now())
                print("Data saved successfully!")  # Debugging line
                return JsonResponse({"message": "Data received successfully"}, status=201)
            else:
                print("Invalid data format:", data)  # Debugging line
                return JsonResponse({"error": "Invalid data format"}, status=400)

        except json.JSONDecodeError:
            print("Invalid JSON received")  # Debugging line
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

def get_sensor_data(request):
    # Get the latest 50 sensor data entries (you can adjust the number if needed)
    sensor_data = SensorData.objects.all().order_by('-timestamp')[:50]
    
    # Convert sensor data to a list of dictionaries
    data_list = [{
        'temperature': data.temperature,
        'humidity': data.humidity,
        'timestamp': data.timestamp.isoformat()
    } for data in sensor_data]
    
    # Return as JSON
    return JsonResponse(data_list, safe=False)

