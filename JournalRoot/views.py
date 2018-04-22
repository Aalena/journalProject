from django.urls import reverse
from django.views.generic import RedirectView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

class Home(RedirectView):
    """
    Homepage. Redirects to login or task list.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if hasattr(self.request, 'user') and self.request.user.is_active:
            return reverse('journals')
        else:
            return reverse('login')

def register(request):
    """
    Registration view. Registers a new user using Django`s built in UserCreationForm
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(request,username=request.POST['username'], password= request.POST['password1'])
            login(request,user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form':form})
