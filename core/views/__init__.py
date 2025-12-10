from .auth import custom_login, logout_view
from .dashboard import dashboard
from .tasks import (
    create_task, edit_task, update_task_status, delete_task, cancel_task,
    submit_result, add_executor, remove_executor, reject_task,
    create_undertask, submit_undertask_result, update_undertask_status, reject_undertask
)
from .events import (
    create_event, delete_event, get_event_participants,
    remove_event_participant, edit_event, add_event_participant
)
from .teams import (
    create_team, add_team_member, remove_team_member, delete_team, get_team_members,
    create_project, complete_project, delete_project, get_project_details, add_project_team, remove_project_team
)
from .users import add_user, delete_user, change_user_role, send_message
from .statistics import view_statistics

__all__ = [
    'custom_login',
    'logout_view',
    'dashboard',
    'create_task',
    'edit_task',
    'update_task_status',
    'delete_task',
    'cancel_task',
    'reject_task',
    'submit_result',
    'add_executor',
    'remove_executor',
    'create_undertask',
    'submit_undertask_result',
    'update_undertask_status',
    'reject_undertask',
    'create_event',
    'delete_event',
    'get_event_participants',
    'remove_event_participant',
    'edit_event',
    'add_event_participant',
    'create_team',
    'add_team_member',
    'remove_team_member',
    'delete_team',
    'get_team_members',
    'create_project',
    'complete_project',
    'delete_project',
    'get_project_details',
    'add_project_team',
    'remove_project_team',
    'add_user',
    'delete_user',
    'change_user_role',
    'send_message',
    'view_statistics',
]
