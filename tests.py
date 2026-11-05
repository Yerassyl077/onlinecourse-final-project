from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Choice, Course, Question, Submission

class ExamTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('learner', password='test-password')
        self.other = get_user_model().objects.create_user('other', password='test-password')
        self.course = Course.objects.create(name='Test course', description='Test')
        self.question = Question.objects.create(course=self.course, question_text='Select both', grade=100)
        self.a = Choice.objects.create(question=self.question, choice_text='A', is_correct=True)
        self.b = Choice.objects.create(question=self.question, choice_text='B', is_correct=True)
        self.c = Choice.objects.create(question=self.question, choice_text='C', is_correct=False)
        self.url = reverse('onlinecourse:submit', args=[self.course.pk])
        self.client.force_login(self.user)

    def test_correct_answers_pass_and_persist(self):
        response = self.client.post(self.url, {'choice_1': [self.a.pk, self.b.pk]}, follow=True)
        self.assertContains(response, 'Congratulations')
        self.assertEqual(response.context['score'], 100)
        self.assertEqual(Submission.objects.get().choices.count(), 2)

    def test_partial_and_extra_answers_fail(self):
        for selected in ([self.a.pk], [self.a.pk, self.b.pk, self.c.pk], []):
            response = self.client.post(self.url, {'choice_1': selected}, follow=True)
            self.assertEqual(response.context['score'], 0)
            self.assertFalse(response.context['passed'])

    def test_foreign_choice_is_rejected(self):
        course = Course.objects.create(name='Other', description='Other')
        question = Question.objects.create(course=course, question_text='Other')
        choice = Choice.objects.create(question=question, choice_text='Other')
        self.assertEqual(self.client.post(self.url, {'choice_1': [choice.pk]}).status_code, 400)
        self.assertEqual(Submission.objects.count(), 0)

    def test_other_user_cannot_read_result(self):
        response = self.client.post(self.url, {'choice_1': [self.a.pk, self.b.pk]})
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(response.url).status_code, 404)

    def test_submit_requires_login_and_post(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)
        self.client.logout()
        self.assertEqual(self.client.post(self.url).status_code, 302)

    def test_invalid_choice_rejected(self):
        self.assertEqual(self.client.post(self.url, {'choice_1': ['invalid']}).status_code, 400)
