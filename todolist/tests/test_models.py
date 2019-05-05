from django.test import TestCase

from todolist.models import Todo

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Todo.objects.create(text='Learn Rest', is_completed='False')

    def test_text_label(self):
        todo = Todo.objects.get(id=1)
        field_label = todo._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'text')

    def test_is_completed_label(self):
        todo = Todo.objects.get(id=1)
        field_label = todo._meta.get_field('is_completed').verbose_name
        self.assertEquals(field_label, 'is completed')

    def test_created_time_label(self):
        todo = Todo.objects.get(id=1)
        field_label = todo._meta.get_field('created_time').verbose_name
        self.assertEquals(field_label, 'created time')

    def test_last_updated_label(self):
        todo = Todo.objects.get(id=1)
        field_label = todo._meta.get_field('last_updated').verbose_name
        self.assertEquals(field_label, 'last updated')

    def test_user_label(self):
        todo = Todo.objects.get(id=1)
        field_label = todo._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    def test_text_max_length(self):
        todo = Todo.objects.get(id=1)
        max_length = todo._meta.get_field('text').max_length
        self.assertEquals(max_length, 400)

    def test_object_name_is_text(self):
        todo = Todo.objects.get(id=1)
        expected_object_name = todo.text
        self.assertEquals(expected_object_name, str(todo))

    def test_get_absolute_url(self):
        todo = Todo.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(todo.get_absolute_url(), '/todolist/todo/1')