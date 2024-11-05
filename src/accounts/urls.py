from django.urls import path
from . import views





app_name = 'accounts'


from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.user_signUp, name='sign_up'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetpassword/', views.resetPassword, name='resetpassword'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit/', views.update_profile, name='update_profile'),

]
