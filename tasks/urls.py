from django.urls import path
from . import views
app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('detail/<int:task_id>', views.detail, name='detail'),
    path('edit/<int:task_id>', views.edit, name='edit'),
    path('delete/<int:task_id>', views.delete, name='delete'),

    path('registration', views.member_registration, name='registration'),
    path('login', views.member_login, name='login'),
    
    path('member-info', views.member_info, name='member_info'),
    path('logout', views.logout_view, name='logout'),
    path('delete-member', views.delete_member_page, name='delete_member'),
    path('remove-member', views.delete_member, name='remove_member'),
    path('update-member', views.profile_update, name='update_member'),
    path('password-change', views.password_change, name='password_change'),
]
