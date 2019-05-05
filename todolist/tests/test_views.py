from django.test import TestCase
from django.urls import reverse
import datetime

from django.utils import timezone
from django.contrib.auth.models import User # Required to assign User as a borrower

from todolist.models import Todo

class TodoListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 todos for pagination tests
        number_of_todos = 13

        for todo_id in range(number_of_todos):
            Todo.objects.create(
                text=f'Todo {todo_id}',
            )
           
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/todolist/')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todolist/todo_list.html')
        
    def test_pagination_is_four(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['todo_list']) == 4)

    def test_lists_all_todos(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('index')+'?page=4')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['todo_list']) == 1)


class TodoByUserListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        
        test_user1.save()
        test_user2.save()

        # Create a todo
        for i in range(10):
            test_todo = Todo.objects.create(user= test_user1, text='Learn Rest', is_completed='False')

    #def setUp(self):
        # Create two users


        # # Create user as a post-step
        # user_objects_for_todo = User.objects.all()
        # test_todo.user.set(user_objects_for_todo) # Direct assignment of many-to-many types not allowed.
        # test_todo.save()
        
    # def test_redirect_if_not_logged_in(self):
    #     response = self.client.get(reverse('index'))
    #     self.assertRedirects(response, '/accounts/login/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('index'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'todolist/todo_list.html')

    def test_only_created_todos_in_list(self):

        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('index'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        
        # Check the object todo_list passed as context
        self.assertTrue('todo_list' in response.context)
        
        # Now change all todos
        todos = Todo.objects.all()[:10]

        for todo in todos:
            todo.is_completed = True
            todo.save()
        
        # Confirm all books belong to testuser1 and completed
        for todo in todos:
            self.assertEqual(response.context['user'], todo.user)
            self.assertEqual(True, todo.is_completed)
