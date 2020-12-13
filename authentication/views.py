import logging

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
logger = logging.getLogger('django')


def RegisterPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        print("post ok")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("post valid")
            form.save()
            user = form.cleaned_data.get('username')
            logger.info('>>>>>>>>>>>>>> le compte de %s a ete bien creer', user)
            messages.success(request, 'le compte de { ' + user + ' } a ete ajoute')
            print("request is_valide")
            return redirect('login')

        else:
            messages.info(request, 'mot de pass inccorecte')
            username = request.POST.get('username')
            logger.warning('>>>>>>>>>>>>>> %s : a essayer de connecter', username)


    context = {'form': form}
    return render(request, 'register.html', context)
