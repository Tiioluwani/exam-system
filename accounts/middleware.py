# accounts/middleware.py

from django.utils.deprecation import MiddlewareMixin
from accounts.permit_utils import sync_user_with_permit
from django.utils.functional import SimpleLazyObject

class ExamPermitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            # If request.user is lazy, unwrap it
            if isinstance(request.user, SimpleLazyObject):
                request.user = request.user._wrapped

            sync_user_with_permit(request.user)
            request.permit_role = request.user.role
