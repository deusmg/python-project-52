from task_manager.test_setup import TaskManagerTestCase


class TestTaskFilter(TaskManagerTestCase):

    def test_only_my_tasks(self):
        response = self.client.get(self.tasks_url, {'only_my_tasks': 'on'})
        self.assertEqual(response.context['tasks'].count(), 0)
        self.client.force_login(self.another_user)
        response = self.client.get(self.tasks_url, {'only_my_tasks': 'on'})
        self.assertEqual(response.context['tasks'].count(), self.count - 1)
        self.assertContains(response, self.task.name)

    def test_filter_by_status(self):
        response = self.client.get(self.tasks_url, {'status': self.status.pk})
        self.assertEqual(response.context['tasks'].count(), self.count - 2)
        self.assertContains(response, self.task.name)
        self.assertNotContains(response, self.task2.name)

    def test_filter_by_executor(self):
        response = self.client.get(
            self.tasks_url,
            {'executor': self.bounded_user.pk}
        )
        self.assertEqual(response.context['tasks'].count(), self.count - 2)
        self.assertContains(response, self.task.name)
        self.assertNotContains(response, self.task2.name)

    def test_filter_by_label(self):
        response = self.client.get(
            self.tasks_url,
            {'labels': self.label.pk}
        )
        self.assertEqual(response.context['tasks'].count(), self.count - 2)
        self.assertContains(response, self.task.name)
        self.assertNotContains(response, self.task2.name)
