from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import AllUsers

User = get_user_model()

class AllUsersModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com"
        )
        self.all_users = AllUsers.objects.create(
            user=self.user,
            first_name="John",
            middle_name="Doe",
            last_name="Smith",
            role=AllUsers.STUDENT,
            is_active=True,
            is_deleted=False
        )

    def test_all_users_creation(self):
        all_users = AllUsers.objects.get(user=self.user)
        self.assertEqual(all_users.first_name, "John")
        self.assertEqual(all_users.middle_name, "Doe")
        self.assertEqual(all_users.last_name, "Smith")
        self.assertEqual(all_users.role, AllUsers.STUDENT)
        self.assertTrue(all_users.is_active)
        self.assertFalse(all_users.is_deleted)

    def test_is_student(self):
        self.assertTrue(AllUsers.is_student(self.user))

    def test_is_lecturer(self):
        # Change the role to lecturer and test
        self.all_users.role = AllUsers.LECTURER
        self.all_users.save()
        self.assertTrue(AllUsers.is_lecturer(self.user))

    def test_is_admissions_team(self):
        # Change the role to admissions team and test
        self.all_users.role = AllUsers.ADMISSIONS_TEAM
        self.all_users.save()
        self.assertTrue(AllUsers.is_admissions_team(self.user))

    def test_is_website_admin(self):
        # Change the role to website admin and test
        self.all_users.role = AllUsers.WEBSITE_ADMIN
        self.all_users.save()
        self.assertTrue(AllUsers.is_website_admin(self.user))