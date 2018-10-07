from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from studdybuddy.models import Skill, CustomUser
from studdybuddy.forms import (
    FullNameForm,
    UserNameForm,
    SkillForm,
    EmailForm,
    PasswordForm,
    StudyPathForm,
    ContactInformationForm
)


def step0(request):
    if request.method == 'POST':
        form = FullNameForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            request.session['full_name'] = full_name
            return redirect(step1)
        else:
            return render(request, 'registration/step-0.html', {'form': form})
    else:
        form = FullNameForm()
        return render(request, 'registration/step-0.html', {'form': form})


def step1(request):
    if request.method == 'POST':
        form = UserNameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            request.session['username'] = username
            return redirect(step2)
        else:
            return render(request, 'registration/step-1.html', {'form': form})
    else:
        form = UserNameForm()
        return render(request, 'registration/step-1.html', {'form': form})


def step2(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.session['email'] = email
            return redirect('step3')
        else:
            return render(request, 'registration/step-2.html', {'form': form})

    else:
        form = EmailForm()
        return render(request, 'registration/step-2.html', {'form': form})


def step3(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            request.session['password'] = password
            return redirect('step4')
        else:
            return render(request, 'registration/step-3.html', {'form': form})
    else:
        form = PasswordForm()
        return render(request, 'registration/step-3.html', {'form': form})


def step4(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skillsiHave = form.cleaned_data['selected_skills']
            request.session['skillsiHave'] = skillsiHave
            return redirect('step5')
        else:
            return render(request, 'registration/step-4.html', {'form': form})
    else:
        form = SkillForm()
        return render(request, 'registration/step-4.html', {'form': form})


def step5(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skillsiWant = form.cleaned_data['selected_skills']
            request.session['skillsiWant'] = skillsiWant

            return redirect('step6')
        else:
            return render(request, 'registration/step-5.html', {'form': form})
    else:
        form = SkillForm()
        return render(request, 'registration/step-5.html', {'form': form})


def step6(request):
    if request.method == 'POST':
        form = StudyPathForm(request.POST)
        if form.is_valid():
            study_path = form.cleaned_data['study_path']
            request.session['study_path'] = study_path

            return redirect('step7')
        else:
            return render(request, 'registration/step-6.html', {'form': form})
    else:
        form = StudyPathForm()
        return render(request, 'registration/step-6.html', {'form': form})


def step7(request):
    if request.method == 'POST':
        form = ContactInformationForm(request.POST)
        if form.is_valid():
            slack_handle = form.cleaned_data['slack_handle']
            phone_number = form.cleaned_data['phone_number']
            request.session['slack_handle'] = slack_handle
            request.session['phone_number'] = phone_number

            # Create & log in the user
            user = createuser(request)
            login(request, user)

            return redirect('profile')
        else:
            return render(request, 'registration/step-7.html', {'form': form})
    else:
        form = ContactInformationForm()
        return render(request, 'registration/step-7.html', {'form': form})


def createuser(request):
    if 'username' in request.session:
        sessionUsername = request.session['username']
    else:
        return HttpResponse("No username")

    if 'email' in request.session:
        sessionEmail = request.session['email']
    else:
        return HttpResponse("No email")

    if 'password' in request.session:
        sesstionPassword = request.session['password']
    else:
        return HttpResponse("No password")

    user = CustomUser.objects.create_user(
        username=sessionUsername,
        email=sessionEmail,
        password=sesstionPassword
    )

    # SKILLS

    if 'skillsiHave' in request.session:
        sesstionskillsiHave = request.session['skillsiHave']
    else:
        return HttpResponse("No teaching skills")

    if 'skillsiWant' in request.session:
        sesstionskillsiWant = request.session['skillsiWant']
    else:
        return HttpResponse("No learning skills")

    for skill in Skill.objects.all():
        if skill.name in sesstionskillsiHave:
            user.iHave.add(skill)
        else:
            user.iHave.remove(skill)

    for skill in Skill.objects.all():
        if skill.name in sesstionskillsiWant:
            user.iWant.add(skill)
        else:
            user.iWant.remove(skill)

    # OPTIONAL INFO

    if 'full_name' in request.session:
        sessionName = request.session['full_name']
        parts = sessionName.split(' ')

        if len(parts) >= 2:
            user.last_name = parts[-1]
            user.first_name = " ".join(parts[:-1])

    if 'slack_handle' in request.session:
        sessionSlack = request.session['slack_handle']
        user.slack_handle = sessionSlack

    if 'phone_number' in request.session:
        sessionPhone = request.session['phone_number']
        user.phone_number = sessionPhone

    user.save()

    user = authenticate(
        username=sessionUsername,
        password=sesstionPassword
    )

    return user
