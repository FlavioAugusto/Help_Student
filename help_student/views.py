# -*- coding:utf-8 -*-
from itertools import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Count, Avg
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from help_student.forms.matter import MatterPeriodForm
from help_student.forms.student import StudentProfileForm
from help_student.forms.student_has_matter import MatterRegisterForm, RankingForm
from help_student.models import StudentHasMatter, Matter


def home(request):
    return direct_to_template(request, template='base.html')


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

            student_matter, has_matter = StudentHasMatter.objects.get_or_create(
                student=request.user,
                matter=form.cleaned_data['matter'])

            student_matter.nr_record = form.cleaned_data['nr_record']
            student_matter.nr_period = form.cleaned_data['nr_period']
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


def teste(query_string):
    cursor = connection.cursor()
    cursor.execute(query_string)
    col_names = [desc[0] for desc in cursor.description]
    row_list = []
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        row_dict = dict(izip(col_names, row))
        # student = teste('select student_id, AVG(nr_record) as media from student_has_matter group by student_id order by -media;')
        row_list.append(row_dict)
    return row_list


@login_required()
def ranking(request):
    student = make_avg()
    if request.POST:
        form = RankingForm(request.POST)
        if form.is_valid():
            # period = form.cleaned_data["nr_period"]
            # matter = form.cleaned_data["matter"]
            # if period:
            #     student = StudentHasMatter.objects.filter(nr_period=period)
            # if matter:
            #     student = StudentHasMatter.objects.filter(matter=matter)
            # if period and matter:
            #     student = StudentHasMatter.objects.filter(nr_period=period, matter=matter,)
            student = make_avg()

    else:
        form = RankingForm()
    return direct_to_template(request, 'ranking.html', {'info': student, 'form': form,})

def make_avg():
    students = User.objects.all()
    student_dict = {}
    for student in students:
        records = StudentHasMatter.objects.filter(student=student).values('nr_record')
        if records:
            for record in records:
                records += record['nr_record']
            student_dict.update({student.id:{'student':student.id, 'record':records}})


    students_avg = {}
    student_list = []
    for student in students:
        if students_avg.has_key(student['student']):
            students_avg[student['student']] += student['student']
        else:
            students_avg[student['student']] = student['student']

    return students_avg