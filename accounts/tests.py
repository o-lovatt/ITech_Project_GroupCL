from django.test import TestCase
from accounts.models import Role, User
# Create your tests here.

#create role test
class Roletest(TestCase):
    def test_role_creation(self):
        test_role = Role.objects.create(role_name = "Guest")
        self.assertEqual(test_role.role_name, "Guest")

class UserTest(TestCase):
    def setUp(self):
        self.test_role = Role.objects.create(role_name = "Receptionist")

    def test_user_creation(self):
        test_user = User.objects.create_user(username = "ollie", password = "password", role = self.test_role)
        self.assertEqual(test_user.username, "ollie")
        self.assertEqual(test_user.role, self.test_role)




        