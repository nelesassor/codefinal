from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from studdybuddy.models import Skill, CustomUser
from studdybuddy.forms import (
    UserNameForm,
    SimpleForm,
    EmailForm,
    PasswordForm
)


def step1(request):
    if request.method == 'POST':
        a = 0
        form = UserNameForm(request.POST)
        if form.is_valid():
            sessionUsername = request.session.get('username', 'NoUsername')
            username = form.cleaned_data['username']
            request.session['username'] = username
            if 'username' in request.session:
                sessionUsername = request.session['username']
            return redirect(step2)
        else:
            return render(request, 'registration/step-1.html', {'form': form})
    else:
        form = UserNameForm()
        a = request.session.keys()
        return render(request, 'registration/step-1.html', {'form': form, 'a': a})


def step2(request):
    if request.method == 'POST':
        a = 0
        form = EmailForm(request.POST)
        if form.is_valid():
            sessionEmail = request.session.get('email', 'NoEmail')
            email = form.cleaned_data['email']
            request.session['email'] = email
            if 'email' in request.session:
                sessionEmail = request.session['email']
            return redirect('step3')
        else:
            return render(request, 'registration/step-2.html', {'form': form})

    else:
        form = EmailForm()
        a = request.session.keys()
        return render(
            request,
            'registration/step-2.html',
            {'form': form, 'a': a}
        )


def step3(request):
    if request.method == 'POST':
        a = 0
        form = PasswordForm(request.POST)
        if form.is_valid():
            sessionPassword = request.session.get('password', 'NoPassword')
            password = form.cleaned_data['password']
            request.session['password'] = password
            if 'password' in request.session:
                a = request.session['password']
            return redirect('step4')
        else:
            return render(request, 'registration/step-3.html', {'form': form})
    else:
        form = PasswordForm()
        a = request.session.keys()
        return render(
            request,
            'registration/step-3.html',
            {'form': form, 'a': a}
        )


def step4(request):
        if request.method == 'POST':
            form = SimpleForm(request.POST)
            if form.is_valid():
                skillsiHave = form.cleaned_data['favorite_skills']
                request.session['skillsiHave'] = skillsiHave
                if 'skillsiHave' in request.session:
                    a = request.session['skillsiHave']
                return redirect('step5')
            else:
                return render(request, 'registration/step-4.html', {'form': form})
        else:
            form = SimpleForm()
            a = request.session.keys()
            return render(
                request,
                'registration/step-4.html',
                {'form': form, 'a': a}
            )


def step5(request):
    if request.method == 'POST':
        form = SimpleForm(request.POST)
        if form.is_valid():
            skillsiWant = form.cleaned_data['favorite_skills']
            request.session['skillsiWant'] = skillsiWant
            if 'skillsiWant' in request.session:
                a = request.session['skillsiWant']
            createuser(request)
            return redirect('profile')
        else:
            return render(request, 'registration/step-5.html', {'form': form})
    else:
        form = SimpleForm()
        a = request.session.keys()
        return render(
            request,
            'registration/step-5.html',
            {'form': form, 'a': a}
        )


def createuser(request):
    if 'username' in request.session:
        sessionUsername = request.session['username']
    else:
        return HttpResponse("kein username")

    if 'email' in request.session:
        sessionEmail = request.session['email']
    else:
        return HttpResponse("kein email")

    if 'password' in request.session:
        sesstionPassword = request.session['password']
    else:
        return HttpResponse("kein password")

    if 'skillsiHave' in request.session:
        sesstionskillsiHave = request.session['skillsiHave']
    else:
        return HttpResponse("kein skillsiHave")

    if 'skillsiWant' in request.session:
        sesstionskillsiWant = request.session['skillsiWant']
    else:
        return HttpResponse("kein skillsiWant")

    user = CustomUser.objects.create_user(
        username=sessionUsername,
        email=sessionEmail,
        password=sesstionPassword
    )

    user = authenticate(
        username=sessionUsername,
        password=sesstionPassword
    )

    login(request, user)

    for skill in Skill.objects.all():
        if skill.name in sesstionskillsiHave:
            request.user.iHave.add(skill)
        else:
            request.user.iHave.remove(skill)

    for skill in Skill.objects.all():
        if skill.name in sesstionskillsiWant:
            request.user.iWant.add(skill)
        else:
            request.user.iWant.remove(skill)
