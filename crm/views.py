from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.

def home(request):
    records = Record.objects.all()

    # checking to know if user is logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #authenticating the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Hello {user} welcome back ')
            return redirect('home')
        else:
            messages.success(request,'There was an Error!')
            return redirect('home')

    else:
        return render(request, 'crm/home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have logged out')
    return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'crm/register.html', {'form':form})

	return render(request, 'crm/register.html', {'form':form})

def customer_record(request, pk):
      if request.user.is_authenticated:
            customer_record = Record.objects.get(id=pk)
            return render(request, 'crm/record.html', {'customer_record':customer_record})
      else:
        messages.success(request, "Login to view!")
        return redirect('home')
      

def delete_record(request, pk):
     if request.user.is_authenticated:
          delete_it = Record.objects.get(id=pk)
          delete_it.delete()
          messages.success(request, "Customer was deleted!")
          return redirect('home')
     else:
          messages.success(request, "Action requires Login")
          return redirect('home')
   
def add_record(request):
     form = AddRecordForm(request.POST or None)
     if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'New Record was added')
                return redirect('home')
          
        return render(request, 'crm/add_record.html', {'form': form})
     
     else:
          messages.success(request, 'Please Login')
          return redirect('home')
     
def update_record(request, pk):
     if request.user.is_authenticated:
          current_record = Record.objects.get(id=pk)
          form = AddRecordForm(request.POST or None, instance=current_record)
          if form.is_valid():
               form.save()
               messages.success(request, 'Record has been updated')
               return redirect('home')
          return render(request, 'crm/update_record.html', {'form': form})
     else:
        messages.success(request, 'Please Login to edit')
        return redirect('home')



