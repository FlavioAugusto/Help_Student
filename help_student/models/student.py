# # -*- coding:utf-8 -*-
# from django.db import models
#
#
# class Student(models.Model):
#     nm_student = models.CharField('Nome', max_length=55)
#     tx_username = models.CharField(u'Usuário', max_length=55, unique=True)
#     tx_password = models.CharField('Senha', max_length=55,)
#
#
#     class Meta:
#         app_label = 'help_student'
#         db_table = 'student'
#         verbose_name = 'Estudante'
#         verbose_name_plural = 'Estudantes'
#
#     def __unicode__(self):
#         return unicode(self.nm_student)