# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from help_student.models.matter import Matter

HELP_CHOICES = (
    (1, 'Preciso de ajuda'),
    (2, 'Posso ajudar'),
)


class StudentHasMatter(models.Model):
    student = models.ForeignKey(User, verbose_name='Estudante')
    matter = models.ForeignKey(Matter, verbose_name=u'Matéria')
    nr_period = models.IntegerField('Ciclo')
    nr_record = models.IntegerField('Nota')
    tp_help = models.SmallIntegerField('Tipo de ajuda', choices=HELP_CHOICES, default=1)

    class Meta:
        app_label = 'help_student'
        db_table = 'student_has_matter'

    def __unicode__(self):
        return unicode(str(self.student.get_full_name()) + ' - ' + str(self.matter))