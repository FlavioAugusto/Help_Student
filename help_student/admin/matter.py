# -*- coding:utf-8 -*-
from django.contrib import admin
from help_student.models import StudentHasMatter
from django.core.mail import send_mail


class MatterAdmin(admin.ModelAdmin):
    actions = ('shot_email_action',)

    def shot_email_action(self, request, queryset):
        for matter in queryset:
            users = list(StudentHasMatter.objects.filter(matter=matter).order_by('-nr_record'))
            users.insert(0, '')
            users_total = len(users) - 1
            for i, user in enumerate(users):
                if user:
                    if i <= (users_total / 2):
                        if user.nr_record >= 60:
                            help_message = u'[Help Student] Ajuar é sempre bom'
                            message = u'Bom dia %s,' \
                                      u'\r o(a) estudante %s precisa de ajuda para estudar %s.' \
                                      u'\r Você poderia adjuda-lo(la) com suas dúvidas?' \
                                      u'\r aqui está o e-mail dele(a) para que possa entrar em contato: %s'

                        else:
                            help_message = u'[Help Student] Não é vergonha alguma perdir ajuda'
                            message = u'Bom dia %s,' \
                                      u'\r o(a) estudante %s pode lhe ajudar à estudar %s.' \
                                      u'\r Você poderia pedir a sua ajuda e tirar suas dúvidas?' \
                                      u'\r aqui está o e-mail dele(a) para que possa entrar em contato: %s'

                        message = message % (
                            users[i].student.get_full_name(),
                            users[-i].student.get_full_name(),
                            matter.nm_matter,
                            users[-i].student.email
                        )
                        send_mail(help_message, message, 'noreplay@help-student.com.br', [users[i].student.email, ])
                    else:
                        break

        self.message_user(request, '%s e-mails foram enviados' % users_total)
    shot_email_action.short_description = 'Enviar e-mails'


