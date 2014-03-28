"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.test import TestCase
from help_student.models import Matter, StudentHasMatter
import mock
import help_student.admin.matter
from help_student.models.student_has_matter import GOOD_NEWS


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class GenericTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user.teste1', password='12345', email='teste1@testes.com.br')
        Matter.objects.create(id=1, nm_matter='materia teste1', nr_difficulty=9)
        Matter.objects.create(id=2, nm_matter='materia teste2', nr_difficulty=3)
        Matter.objects.create(id=3, nm_matter='materia teste3', nr_difficulty=4)
        self.client.login(username='user.teste1', password='12345')

    def test_registra_materia(self):
        shm = StudentHasMatter.objects.all()
        self.assertEquals(shm.count(), 0)

        data = {
            'matter': 1,
            'nr_period': 0,
            'nr_record': 10,
        }
        response = self.client.post(reverse('materia'), data=data)

        self.assertEquals(response.status_code, 200)

        shm = StudentHasMatter.objects.all()
        self.assertEquals(shm.count(), 1)

    def test_edita_materia(self):
        data = {
            'matter': 1,
            'nr_period': 0,
            'nr_record': 10,
        }
        self.client.post(reverse('materia'), data=data)
        shm = StudentHasMatter.objects.all()

        self.assertEquals(shm.count(), 1)
        self.assertEquals(shm[0].matter_id, 1)
        self.assertEquals(shm[0].nr_period, 0)
        self.assertEquals(shm[0].nr_record, 10)

        data['nr_period'] = 1
        data['nr_record'] = 60

        self.client.post(reverse('materia'), data=data)
        shm = StudentHasMatter.objects.all()

        self.assertEquals(shm.count(), 1)
        self.assertEquals(shm[0].matter_id, 1)
        self.assertEquals(shm[0].nr_period, 1)
        self.assertEquals(shm[0].nr_record, 60)

    def test_estudante_precisa_de_ajuda(self):
        data = {
            'matter': 1,
            'nr_period': 0,
            'nr_record': 10,
        }
        self.client.post(reverse('materia'), data=data)
        shm = StudentHasMatter.objects.all()

        self.assertEquals(shm.count(), 1)
        self.assertEquals(shm[0].tp_help, 1)

    def test_estudante_pode_ajudar(self):
        data = {
            'matter': 1,
            'nr_period': 0,
            'nr_record': 60,
        }
        self.client.post(reverse('materia'), data=data)
        shm = StudentHasMatter.objects.all()

        self.assertEquals(shm.count(), 1)
        self.assertEquals(shm[0].tp_help, 2)

    def test_retorna_todas_as_materias(self):
        response = self.client.get(reverse('status'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['user'].studenthasmatter_set.all().count(), 0)

        data = {
            'matter': 1,
            'nr_period': 0,
            'nr_record': 60,
        }

        self.client.post(reverse('materia'), data=data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['user'].studenthasmatter_set.all().count(), 1)

    def test_retorna_materias_de_um_periodo(self):
        data = {
            'matter': 1,
            'nr_period': 1,
            'nr_record': 60,
        }
        data2 = {
            'matter': 2,
            'nr_period': 1,
            'nr_record': 60,
        }
        data3 = {
            'matter': 3,
            'nr_period': 3,
            'nr_record': 60,
        }
        data_post = {
            'nr_period': 1
        }

        response = self.client.get(reverse('status'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['user'].studenthasmatter_set.all().count(), 0)

        self.client.post(reverse('materia'), data=data)
        self.client.post(reverse('materia'), data=data2)
        self.client.post(reverse('materia'), data=data3)

        response = self.client.get(reverse('status'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['user'].studenthasmatter_set.all().count(), 3)

        response = self.client.post(reverse('status'), data=data_post)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['user'].studenthasmatter_set.filter(nr_period=1).count(), 2)

    def test_envia_email(self):
        user = User.objects.create_user(username='user.teste2', password='12345', email='teste2@testes.com.br')
        StudentHasMatter.objects.create(student_id=1, matter_id=1, nr_period=0, nr_record=70, tp_help=2)
        StudentHasMatter.objects.create(student_id=2, matter_id=1, nr_period=0, nr_record=40, tp_help=1)

        with mock.patch.object(help_student.admin.matter, 'send_mail'):
            matter = Matter.objects.filter(id=1)
            help_student.admin.MatterAdmin(mock.MagicMock(), mock.MagicMock()).shot_email_action(mock.MagicMock(), matter)
            self.assertEquals(help_student.admin.matter.send_mail.call_count, 1)

            message = GOOD_NEWS['message'] % (
                'user.teste1',
                'user.teste2',
                'materia teste1',
                'teste2@testes.com.br'
            )
            my_mock = mock.call(GOOD_NEWS['subject'], message, 'noreplay@help-student.com.br', ['teste1@testes.com.br'])
            self.assertEquals([my_mock], help_student.admin.matter.send_mail.call_args_list)
#AssertionError: [
#                    call(u'[Help Student] Ajuar \xe9 sempre bom', u'Bom dia user.teste1,\r o(a) estudante user.teste2 precisa de ajuda para estudar materia teste1.\r Voc\xea poderia adjuda-lo(la) com suas d\xfavidas?\r aqui est\xe1 o e-mail dele(a) para que possa entrar em contato: teste2@testes.com.br', 'noreplay@help-student.com.br', ['teste1@testes.com.br'])
#                ] ![call(u'[Help Student] Ajuar \xe9 sempre bom', u'Bom dia            ,\r o(a) estudante             precisa de ajuda para estudar materia teste1.\r Voc\xea poderia adjuda-lo(la) com suas d\xfavidas?\r aqui est\xe1 o e-mail dele(a) para que possa entrar em contato: teste2@testes.com.br', 'noreplay@help-student.com.br', [u'teste1@testes.com.br'])]
