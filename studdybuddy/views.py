from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import Skill, CustomUser
from random import randint
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from itertools import chain
from django.contrib.auth import login, authenticate

from .forms import CustomUserCreationForm, CustomUserChangeForm, UserNameForm, SimpleForm, EmailForm, PasswordForm

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class userchange(generic.CreateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('index')
    template_name = 'changeuser.html'

def landing(request):
    return render(request, 'landing.html', context=context)

@login_required
def index(request):
    currentUser = request.user
    a = 0
    if currentUser.machted == False:
        a=1
        i = 1
        skills = currentUser.iWant.all()
        numberOfSkills = len(skills)
        if numberOfSkills == 0:
            text ="pick a skill you want to learn to find a match"
            context = {
                'numberOfSkills': numberOfSkills,
                'text': text
            }
            return render(request, 'index.html', context=context)
        else:
            matches = skills[0].iWant.exclude(username=request.user.username)
            while i <= len(currentUser.iWant.all()) - 1:
                matches = matches | skills[i].iHave.exclude(username=request.user.username)
                i += 1
            matches.exclude(username=request.user.username)
            if CustomUser.objects.filter(machted = True).exists():
                for alreadyMatched in CustomUser.objects.filter(machted=True):
                    matches.exclude(username=alreadyMatched.username)

            if len(matches) == 0:
                text = "currently no matches"
                numberOfSkills = 0
                context = {
                    'numberOfSkills': numberOfSkills,
                    'text': text
                }
                return render(request, 'index.html', context=context)

            matches1 = matches
            # gibt es ein Rematch
            for user in matches:
                for skill in user.iWant.all():
                    if skill not in currentUser.iHave.all():
                        matches.exclude(username=user)

        if len(matches) == 0:
            text = "currently no matches"
            numberOfSkills = 0
            context = {
                'numberOfSkills': numberOfSkills,
                'text': text
            }
            return render(request, 'index.html', context=context)
        else:
            randomNumber = randint(0, len(matches) - 1)
            matched_user = matches[randomNumber]

        matched_user.machtedUserID = currentUser.post_id
        matched_user.machted = True
        matched_user.save()
        currentUser.machted = True
        currentUser.matchedUserID = matched_user.post_id
        currentUser.save()
        setMatchedId(currentUser)
        a1 = matches1
        a = matches
        all_skills_iHave = matched_user.iHave.all()
        all_skills_iWant = matched_user.iWant.all()
    else:
        a1=2
        a=2
        matched_id = request.user.matchedUserID
        matched_user = CustomUser.objects.get(post_id=matched_id)
        matched_user.save()
        all_skills_iHave = matched_user.iHave.all()
        all_skills_iWant = matched_user.iWant.all()


    context = {
        'matched_user': matched_user,
        'all_skills_iHave': all_skills_iHave,
        'all_skills_iWant': all_skills_iWant,
        'a': a,
        'a1': a1
    }

    return render(request, 'index.html', context = context)


@login_required
def profile(request):
    all_skills_iHave = request.user.iHave.all()
    all_skills_iWant = request.user.iWant.all()
    current_user = request.user

    context = {
        'current_user': current_user,
        'all_skills_iHave': all_skills_iHave,
        'all_skills_iWant': all_skills_iWant,
    }

    return render(request, 'profile.html', context = context)

@login_required
def profileEdit(request):
    all_skills_iHave = request.user.iHave.all()
    all_skills_iWant = request.user.iWant.all()
    current_user = request.user

    context = {
        'current_user': current_user,
        'all_skills_iHave': all_skills_iHave,
        'all_skills_iWant': all_skills_iWant,
    }

    return render(request, 'profile-edit.html', context = context)


@login_required
def edit(request):
    if request.method == 'POST':
        form = SimpleForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['favorite_skills']
            for skill in Skill.objects.all():
                if skill.name in a:
                    request.user.iHave.add(skill)
                else:
                    request.user.iHave.remove(skill)

            currentUser = request.user
            if (currentUser.matchedUserID != '') & (currentUser.matchedUserID != '0'):
                matchedUser = CustomUser.objects.get(post_id=currentUser.matchedUserID)
                currentUser.machted = False
                matchedUser.machted = False
                currentUser.matchedUserID = 0
                matchedUser.matchedUserID = 0
                currentUser.save()
                matchedUser.save()

        return redirect('edit2')
    else:
        form = SimpleForm()
        return render(request, 'sign-in/step-4.html', {'form': form} )


@login_required
def edit2(request):
    if request.method == 'POST':
        form = SimpleForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['favorite_skills']
            for skill in Skill.objects.all():
                if skill.name in a:
                    request.user.iWant.add(skill)
                else:
                    request.user.iWant.remove(skill)

            currentUser = request.user
            if (currentUser.matchedUserID != '') & (currentUser.matchedUserID != '0'):
                matchedUser = CustomUser.objects.get(post_id=currentUser.matchedUserID)
                currentUser.machted = False
                matchedUser.machted = False
                currentUser.matchedUserID = 0
                matchedUser.matchedUserID = 0
                currentUser.save()
                matchedUser.save()

        return redirect('profile')
    else:
        form = SimpleForm()
        return render(request, 'sign-in/step-5.html', {'form': form})

def step1(request):
    if request.method == 'POST':
        a=0
        form = UserNameForm(request.POST)
        if form.is_valid():
            sessionUsername = request.session.get('username', 'NoUsername')
            username = form.cleaned_data['username']
            request.session['username'] = username
            if 'username' in request.session:
                sessionUsername = request.session['username']
            return redirect(step2)
        else:
            return render(request, 'sign-in/step-1.html', {'form': form})
    else:
        form = UserNameForm()
        a = request.session.keys()
        return render(request, 'sign-in/step-1.html', {'form': form, 'a': a})


def step2(request):
    if request.method == 'POST':
        a=0
        form = EmailForm(request.POST)
        if form.is_valid():
            sessionEmail = request.session.get('email', 'NoEmail')
            email = form.cleaned_data['email']
            request.session['email'] = email
            if 'email' in request.session:
                sessionEmail = request.session['email']
            return redirect('step3')
        else:
            return render(request, 'sign-in/step-2.html', {'form': form})

    else:
        form = EmailForm()
        a = request.session.keys()
        return render(request, 'sign-in/step-2.html', {'form': form, 'a':a})

def step3(request):
    if request.method == 'POST':
        a=0
        form = PasswordForm(request.POST)
        if form.is_valid():
            sessionPassword = request.session.get('password', 'NoPassword')
            password = form.cleaned_data['password']
            request.session['password'] = password
            if 'password' in request.session:
                a = request.session['password']
            return redirect('step4')
        else:
            return render(request, 'sign-in/step-3.html', {'form': form})
    else:
        form = PasswordForm()
        a = request.session.keys()
        return render(request, 'sign-in/step-3.html', {'form': form, 'a':a})

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
                return render(request, 'sign-in/step-4.html', {'form': form})
        else:
            form = SimpleForm()
            a = request.session.keys()
            return render(request, 'sign-in/step-4.html', {'form': form, 'a':a})


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
            return render(request, 'sign-in/step-5.html', {'form': form})
    else:
        form = SimpleForm()
        a = request.session.keys()
        return render(request, 'sign-in/step-5.html', {'form': form, 'a': a})

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

    user = CustomUser.objects.create_user(username=sessionUsername,
                                    email=sessionEmail,
                                    password=sesstionPassword)

    user = authenticate(username=sessionUsername, password=sesstionPassword)
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









def setMatchedId(currentUser):
    matchedUser = CustomUser.objects.get(post_id=currentUser.matchedUserID)
    matchedUser.matchedUserID = currentUser.post_id
    matchedUser.save()
