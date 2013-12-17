# -*- coding:utf-8 -*-
from django.contrib import admin
from Help_Student import settings
from help_student.models import StudentHasMatter
from django.core.mail import send_mail
from help_student.models.student_has_matter import GOOD_NEWS, BAD_NEWS


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
                            help_message = GOOD_NEWS['subject']
                            message = GOOD_NEWS['message']

                        else:
                            help_message = BAD_NEWS['message']
                            message = BAD_NEWS['message']
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


    # def get_matter_view(self):
    #     from splinter import Browser