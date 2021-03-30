from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.common_myForms import MyUserForm

# Create your views here.



def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = MyUserForm(request.POST)
        if form.is_valid():  #UserCreationForm.is_valid()함수
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = MyUserForm()
    return render(request, 'common/signup.html', {'form': form})
