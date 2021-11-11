from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from api.models import UserInfo


class UpdateLastRequestMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            UserInfo.objects.filter(user=request.user.id).update_or_create(
                user=User.objects.get(id=request.user.id),
                defaults={"last_request": timezone.now()}
            )

        return response

