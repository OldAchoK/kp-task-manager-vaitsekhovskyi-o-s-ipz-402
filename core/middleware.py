import logging
from django.db import connection

logger = logging.getLogger(__name__)

class RoleSwitchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_role = request.session.get('db_role', 'connect_user')
        safe_role = user_role.replace(' ', '')
        allowed_roles = ['connect_user', 'Individual', 'Developer', 'Manager', 'Lead']

        if safe_role not in allowed_roles:
            safe_role = 'connect_user'

        with connection.cursor() as cursor:
            sql = f'SET ROLE "{safe_role}"'
            cursor.execute(sql)
            logger.info(f" >>> [Middleware] Role switched to: {safe_role}")

        response = self.get_response(request)

        with connection.cursor() as cursor:
            cursor.execute("RESET ROLE")

        return response