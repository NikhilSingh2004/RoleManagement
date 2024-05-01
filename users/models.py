from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    """
        Creating an Role Table that will have multiple roles for the Users
        Every Role in the Role tables should be unique
        The ID Field will be automatically implemented by the user
    """
    name = models.CharField(max_length=100, unique=True)

class User(AbstractUser):
    """
        The default User module will be user django.contrib.auth.model.User
        Will create an Abstract user through the Default user will role filed in the model
        The Inactive filed if set to True then users is NOT ACTIVE and not using the system, if False the User is ACTIVE
    """
    roles = models.ManyToManyField(Role, through='UserRole')
    inactive = models.BooleanField(default=False)

class UserRole(models.Model):
    """
        The UserRole Table is a log tables that will keep note of all the transactions done with assigning role and who have got the role
        I also have to implement and status field that will showcase the user's activiness
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
