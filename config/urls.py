from django.urls import path
from core import views

urlpatterns = [
    path('', views.custom_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('statistics/', views.view_statistics, name='statistics'),

    path('task/create/', views.create_task, name='create_task'),
    path('task/edit/', views.edit_task, name='edit_task'),
    path('task/update/', views.update_task_status, name='update_task'),
    path('task/reject/', views.reject_task, name='reject_task'),
    path('task/delete/', views.delete_task, name='delete_task'),
    path('task/submit/', views.submit_result, name='submit_result'),
    path('task/cancel/', views.cancel_task, name='cancel_task'),
    path('task/add_executor/', views.add_executor, name='add_executor'),
    path('task/remove_executor/', views.remove_executor, name='remove_executor'),

    path('undertask/create/', views.create_undertask, name='create_undertask'),
    path('undertask/submit/', views.submit_undertask_result, name='submit_undertask'),
    path('undertask/update/', views.update_undertask_status, name='update_undertask'),
    path('undertask/reject/', views.reject_undertask, name='reject_undertask'),

    path('event/create/', views.create_event, name='create_event'),
    path('event/edit/', views.edit_event, name='edit_event'),
    path('event/delete/', views.delete_event, name='delete_event'),
    path('event/participants/<int:event_id>/', views.get_event_participants, name='event_participants'),
    path('event/add_participant/', views.add_event_participant, name='add_event_participant'),
    path('event/remove_participant/', views.remove_event_participant, name='remove_event_participant'),

    path('message/send/', views.send_message, name='send_message'),

    path('user/add/', views.add_user, name='add_user'),
    path('user/delete/', views.delete_user, name='delete_user'),
    path('user/change_role/', views.change_user_role, name='change_user_role'),

    path('team/create/', views.create_team, name='create_team'),
    path('team/delete/', views.delete_team, name='delete_team'),
    path('team/members/<int:team_id>/', views.get_team_members, name='get_team_members'),
    path('team/add_member/', views.add_team_member, name='add_team_member'),
    path('team/remove_member/', views.remove_team_member, name='remove_team_member'),

    path('project/create/', views.create_project, name='create_project'),
    path('project/complete/', views.complete_project, name='complete_project'),
    path('project/delete/', views.delete_project, name='delete_project'),
    path('project/details/<int:project_id>/', views.get_project_details, name='get_project_details'),
    path('project/add_team/', views.add_project_team, name='add_project_team'),
    path('project/remove_team/', views.remove_project_team, name='remove_project_team'),
]