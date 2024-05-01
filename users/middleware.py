from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import UserRole

class UserActivityMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)

    def __call__(self, request):
        # Capture login/logout events
        user_logged_in.connect(self.log_user_login)
        user_logged_out.connect(self.log_user_logout)

        # Capture role changes
        post_save.connect(self.log_role_change, sender=UserRole)
        pre_delete.connect(self.log_role_removal, sender=UserRole)

        response = self.get_response(request)
        return response

    def log_user_login(sender, request, user, **kwargs):
        UserRole.objects.create(user=user, action='LOGIN')

    def log_user_logout(sender, request, user, **kwargs):
        UserRole.objects.create(user=user, action='LOGOUT')

    def log_role_change(sender, instance, created, **kwargs):
        if created:
            action = 'ASSIGNED'
        else:
            action = 'UPDATED'
        UserRole.objects.create(user=instance.user, action=f'ROLE_{action}', role=instance.role)

    def log_role_removal(sender, instance, **kwargs):
        UserRole.objects.create(user=instance.user, action='ROLE_REMOVED', role=instance.role)
