import logging
from django.db import connection

logger = logging.getLogger(__name__)


class RoleSwitchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        db_user = request.session.get('db_user', 'connect_user')

        safe_user = db_user.replace(' ', '').replace('"', '').replace(';', '')
        if safe_user != 'connect_user' and not safe_user.startswith('user_'):
            safe_user = 'connect_user'

        with connection.cursor() as cursor:
            sql = f'SET ROLE "{safe_user}"'
            try:
                cursor.execute(sql)
                logger.info(f" >>> [Middleware] Role switched to: {safe_user}")
            except Exception as e:
                logger.error(f"Failed to switch role to {safe_user}: {e}")

        response = self.get_response(request)

        with connection.cursor() as cursor:
            cursor.execute("RESET ROLE")

        return response