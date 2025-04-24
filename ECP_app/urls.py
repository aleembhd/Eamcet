from django.urls import path,include
from . import views
urlpatterns = [
	path('',views.homepage,name='home'),
	path('login/', views.login_view, name='login'),
	path('signup/', views.signup_view, name='signup'),
	path('logout/', views.logout_view, name='logout'),
	path('auth/callback/', views.auth_callback, name='auth_callback'),
	path('colleges/',views.college_list,name='colleges'),
	path('college/<str:pk>/',views.college_branch,name='college_branch'),
	path('college-branch-student/', views.college_branch_student_view, name='college_branch_student'),
	path('college-guide/', views.college_guide, name='college_guide'),
	path('chat/', views.chat, name='chat'),
]