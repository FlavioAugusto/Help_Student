# -*- coding:utf-8 -*-
from django import forms
from help_student.models import Matter


class MatterRegisterForm(forms.ModelForm):
    matter = forms.ModelChoiceField(queryset=Matter.objects.all(), label=u'Matéria')
    nr_period = forms.IntegerField(label=u'Ciclo')
    nr_record = forms.IntegerField(label=u'Nota')

    class Meta:
        model = Matter
        fields = ('matter', 'nr_period', 'nr_record')

    def __init__(self, *args, **kwargs):
        super(MatterRegisterForm, self).__init__(*args, **kwargs)


class RankingForm(forms.ModelForm):
    matter = forms.ModelChoiceField(queryset=Matter.objects.all(), label=u'Matéria', required=False)
    nr_period = forms.IntegerField(label=u'Ciclo', required=False)

    class Meta:
        model = Matter
        fields = ('matter', 'nr_period')

    def __init__(self, *args, **kwargs):
        super(RankingForm, self).__init__(*args, **kwargs)
