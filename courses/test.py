from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Course, Step


class CourseModelTest(TestCase):
    def test_course_creation(self):
        course = Course.objects.create(
            title="Python Regular Expressions",
            description="Learn to write regular expressions in Python"
        )
        now = timezone.now()
        self.assertLess(course.created_at, now)

class StepModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python Testing",
            description="Learn to write python tests ",
        )

    def test_step_creation(self):
        step = Step.objects.create(
            title="Introduction to Doctests",
            description="Learn to write tests in the doc strings",
            course=self.course
        )
        self.assertIn(step, self.course.step_set.all())


class CourseViewsTests(TestCase):
    """ This is a view and template test """
    def setUp(self):
        self.first_course = Course.objects.create(
            title="Python Testing",
            description="Learn to write tests in Python"
        )
        self.second_course = Course.objects.create(
            title="New Course",
            description="A new course"
        )
        self.step = Step.objects.create(
            title="Introdution to Doctests",
            description="Learn to write tests in your docstrings.",
            course=self.first_course
        )

    def test_course_list_view(self):
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.first_course, response.context['courses'])
        self.assertIn(self.second_course, response.context['courses'])
        self.assertTemplateUsed(response, 'courses/course_list.html')
        self.assertContains(response, self.first_course.title)

    def test_course_detail_view(self):
        response = self.client.get(
            reverse(
                'courses:course_detail',
                kwargs={'pk': self.first_course.pk},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.first_course, response.context['course'])

    def test_step_detail(self):
        response = self.client.get(
            reverse(
                'courses:step_detail',
                kwargs={
                    'course_pk': self.first_course.pk,
                    'step_pk': self.step.pk
                }
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.step, response.context['step'])
