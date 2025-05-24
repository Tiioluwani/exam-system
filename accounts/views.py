from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm
from .permit_utils import sync_user_with_permit  # This is the helper function that syncs the user to Permit

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Saves the user and assigns the role
            # Sync the user with Permit.io
            sync_user_with_permit(user)
            return redirect('login')  # Redirect to login after registration
    else:
        form = StudentRegistrationForm()  # Empty form if the method is GET
    
    return render(request, 'accounts/register.html', {'form': form})
