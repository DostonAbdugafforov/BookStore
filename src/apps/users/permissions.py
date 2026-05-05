from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import CustomUser


class IsAdmin(BasePermission):
    message = "Faqat adminlar uchun."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and str(request.user.role).upper() == "ADMIN"
        )
