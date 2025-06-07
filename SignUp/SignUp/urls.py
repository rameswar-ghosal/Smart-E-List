"""SignUp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from enroll import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.sel, name="sel"),
    path('home', views.home, name="home"),
    path('pin_unpin/<int:id>/', views.pinned, name="pin_unpin"),
    path('pin_unpinJ', views.pinnedJ, name="pin_unpinJ"),
    path('C_home', views.C_home, name="C_home"),
    path('roomcreated/', views.room_created, name="roomcreated"),
    path('user_in_ur_room/',views.user_in_ur_room, name="user_in_ur_room"),
    path('room_am_in/',views.room_am_in,name="room_am_in"),
    path('userdelete/', views.userdelete, name="userdelete"),
    path('usermanage/', views.usermanage, name="usermanage"),
    path('userinwait', views.userinwait, name="userinwait"),
    path('adm_reaction', views.adm_reaction, name="adm_reaction"),
    #path('checkview', views.checkview, name="checkview"),
    path('inside_r/<str:room>/', views.room, name='room'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),

    path('SignUp/', views.sign_up,name='sign_up'),
    path('help/', views.help,name='help'),
   # path(''+'<int:my_id>/',views.sign_up,name='signing_up'),
    path('r_no/',views.r_no_generation,name='r_no'),
    path('e_uq/<int:id>/', views.e_u_key, name='ed_uq'),
    path('gen_uk/<int:id>/', views.gen_unique_key,name="gen_uk"),
    path('login/<int:id>/', views.user_login,name="login"),
    path('profile/', views.user_profile,name="profile"),
    path('logout/', views.user_logout,name="logout"),
    path('changepass/', views.user_password,name="changepass"),
    path('changepass1/', views.user_password1, name="changepass1"),
    path('delete/<int:id>/',views.delete_data,name='deletedata'),
    path('<int:id>/',views.update_data,name='updatedata'),
    path("Update_City/<int:id>/",views.update_city,name='updatecity'),
    path('import/', views.importandsee, name='import'),
    path('export/', views.export_data, name='export'),
    path('sending_email/', views.sending_email, name="email"),
    path('About_me/', views.AboutMe, name="aboutme"),
    path('Search/', views.scrape, name="search"),
    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='enroll/password_reset_form.html',
             subject_template_name='enroll/password_reset_subject.txt',
             email_template_name='enroll/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='enroll/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='enroll/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='enroll/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
