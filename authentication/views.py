from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from codes.forms import CodeForm
from users.models import CustomUser


@login_required
def home(request):
    return render(requestm, 'main.html', {})


def auth_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username   = request.POST.get('username')
        password   = request.POST.get('password')
        user       = authenticate(username=username, password=password)

        if user is not None:
            request.session['pk'] = user.pk
            return redirect('verify')
    return render(request, 'auth.html', {'form':form})


def verify(request):
    form = CodeForm()

    form = CodeForm(request.POST or None)
    pk   = request.session.get('pk')

    if pk:
        user = CustomUser.objects.get(pk=pk)
        code      = user.code
        code_user = f"{user.username} : {code}"

        if not request.POST:
            print(code) 
            # SEND SMS
        if form.is_valid():
            num = form.cleaned_data.get('number')  

            if code == num:
                code.save()
                login(request, user)
                return redirect('main')
            else:
                return redirect('login')
    return render(request, 'verify.html', {'form':form})
