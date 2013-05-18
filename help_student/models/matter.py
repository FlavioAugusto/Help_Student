# -*- coding:utf-8 -*-
from django.db import models


class Matter(models.Model):
    nm_matter = models.CharField(u'Matéria', max_length=55)
    nr_difficulty = models.IntegerField('Dificuldade')

    class Meta:
        app_label = 'help_student'
        db_table = 'matter'
        verbose_name = u'Matéria'
        verbose_name_plural = u'Matérias'

    def __unicode__(self):
        return self.nm_matter