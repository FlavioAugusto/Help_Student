# -*- coding:utf-8 -*-
from django import forms


class MatterPeriodForm(forms.Form):
    nr_period = forms.IntegerField(label='Ciclo')
