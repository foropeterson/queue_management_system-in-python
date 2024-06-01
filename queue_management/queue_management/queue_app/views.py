from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Customer, QueueEntry, CustomerVisit
from .forms import CustomerForm
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login

@login_required
def home(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            QueueEntry.objects.create(customer=customer)
            return redirect('queue_status')
    else:
        form = CustomerForm()
    return render(request, 'queue_app/home.html', {'form': form})

@login_required
def queue_status(request):
    queue_entries = QueueEntry.objects.order_by('timestamp')
    served_entries = QueueEntry.objects.filter(served=True).order_by('-timestamp')[:1]  # Show the last served customer
    return render(request, 'queue_app/queue_status.html', {'queue_entries': queue_entries, 'served_entries': served_entries})

@login_required
def invite_next(request):
    # Find the first uninvited and unserved entry
    next_entry = QueueEntry.objects.filter(invited=False, served=False).order_by('timestamp').first()
    if next_entry:
        next_entry.invited = True
        next_entry.desk = assign_desk()
        next_entry.save()
    return redirect('queue_status')

@login_required
def serve_customer(request):
    # Find the first invited and unserved entry
    current_entry = QueueEntry.objects.filter(invited=True, served=False).order_by('timestamp').first()
    if current_entry:
        current_entry.served = True
        current_entry.save()

        # Automatically invite the next customer
        invite_next(request)

        # Display the thank you message and update the queue status page
        return render(request, 'queue_app/thank_you.html', {'customer': current_entry.customer})

    return redirect('queue_status')

@login_required
def direct_to_desk(request, desk):
    # Here you can implement the logic to direct the customer to their allocated desk
    # This could include displaying instructions or redirecting to another page
    return render(request, 'queue_app/direction.html', {'desk_number': desk})

@login_required
def logout(request):
    # Calculate visit duration
    visit = CustomerVisit.objects.filter(customer=request.user).order_by('-start_time').first()
    if visit:
        duration = timezone.now() - visit.start_time
        if duration.total_seconds() > 5 * 60:  # 5 minutes
            # Log out the customer and remove them from the queue
            visit.delete()
            return redirect('logout_success')
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page, or a login page
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def assign_desk():
    assigned_desks = QueueEntry.objects.filter(invited=True, served=False).values_list('desk', flat=True)
    for desk in range(1, 30):
        if desk not in assigned_desks:
            return desk
    return None
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                CustomerVisit.objects.create(customer=request.user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})
def allocate_next_user(request):
    # Logic to allocate the next user goes here
    # For example, you can write code to fetch the next user from the queue
    # and perform any necessary actions
    
    # After performing the necessary actions, redirect back to the queue status page
    return redirect('queue_status')