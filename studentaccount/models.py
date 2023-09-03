from django.db import models
from base.manager import UserManager
from django.contrib.auth import get_user_model

User = get_user_model()

class AllUsers(models.Model):
    STUDENT = 'student'
    LECTURER = 'lecturer'
    ADMISSIONS_TEAM = 'admissions_team'
    WEBSITE_ADMIN = 'website_admin'

    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (LECTURER, 'Lecturer'),
        (ADMISSIONS_TEAM, 'Admissions Team'),
        (WEBSITE_ADMIN, 'Website Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def is_student(user):
        return user.allusers.role == 'student'

    @staticmethod
    def is_lecturer(user):
        return user.allusers.role == 'lecturer'

    @staticmethod
    def is_admissions_team(user):
        return user.allusers.role == 'admissions_team'

    @staticmethod
    def is_website_admin(user):
        return user.allusers.role == 'website_admin'

    def __str__(self):
        return self.first_name


