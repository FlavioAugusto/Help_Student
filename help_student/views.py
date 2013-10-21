# -*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from help_student.forms.matter import MatterPeriodForm
from help_student.forms.student import StudentProfileForm
from help_student.forms.student_has_matter import MatterRegisterForm, RankingForm
from help_student.models import StudentHasMatter


def home(request):
    return direct_to_template(request, 'base.html',)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('../accounts/profile')
    else:
        form = UserCreationForm()
    return direct_to_template(request, 'register_form.html', {'form': form, 'legend': 'Cadastro'})

@login_required()
def profile(request):
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return direct_to_template(request, 'register_form.html', {'form': form, 'message': 'Aterado com Sucesso', 'legend': 'Perfil'})
    else:
        form = StudentProfileForm(instance=request.user)
    return direct_to_template(request, 'register_form.html', {'form': form, 'legend': 'Perfil'})

@login_required()
def register_matter(request):
    if request.method == 'POST':
        form = MatterRegisterForm(request.POST)
        message = ''
        if form.is_valid():
            if form.cleaned_data['nr_record'] >= 60:
                tp_help = 2
            else:
                tp_help = 1
            nr_record = form.cleaned_data['nr_record']
            nr_period = form.cleaned_data['nr_period']

            student_matter, has_matter = StudentHasMatter.objects.get_or_create(
                student=request.user,
                matter=form.cleaned_data['matter'], defaults={'nr_record': nr_record, 'nr_period': nr_period})

            student_matter.nr_record = nr_record
            student_matter.nr_period = nr_period
            student_matter.tp_help = tp_help
            student_matter.save()

            if has_matter:
                message = u'Matéria criada com sucesso'
            else:
                message = u'Matéria editada com sucesso'

        return direct_to_template(request, 'register_form.html', {'form': form, 'message': message, 'legend': u'Registrar Matéria'})

    else:
        form = MatterRegisterForm()

    return direct_to_template(request, 'register_form.html', {'form': form, 'legend': u'Registrar Matéria'})


@login_required
def status_matter(request):
    student = StudentHasMatter.objects.filter(student=request.user).order_by('nr_period', '-nr_record')
    if request.POST:
        form = MatterPeriodForm(request.POST)
        if form.is_valid():
            student = student.filter(nr_period=form.cleaned_data["nr_period"])
    else:
        form = MatterPeriodForm()

    return direct_to_template(request, 'status_matter.html', {'info': student, 'form': form})


@login_required()
def ranking(request):

    if request.POST:
        form = RankingForm(request.POST)
        if form.is_valid():
            period = form.cleaned_data["nr_period"]
            matter = form.cleaned_data["matter"]
            if period and matter:
                student = StudentHasMatter.objects.filter(nr_period=period, matter=matter,)
            elif period:
                student = StudentHasMatter.objects.filter(nr_period=period)
            elif matter:
                student = StudentHasMatter.objects.filter(matter=matter)
            else:
                student = StudentHasMatter.objects.all()
            student = make_avg(student)

    else:
        form = RankingForm()
        student = StudentHasMatter.objects.all()
        student = make_avg(student)

    return direct_to_template(request, 'ranking.html', {'infos': student, 'form': form, })


def make_avg(students):
    student_list = list()
    for student in students:
        new_record = 0
        records = students.filter(student_id=student.student.id).values('nr_record')
        if records:
            for record in records:
                new_record += record['nr_record']
            new_record = new_record / len(records)
            new = {'student': student.student.get_full_name(), 'record': new_record}
            if new not in student_list:
                student_list.append(new)

    student_list.sort(reverse=True)
    return student_list[:10]

