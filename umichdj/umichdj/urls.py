"""umich_dj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
# from django.contrib.auth import views as auth_views
from django.views.static import serve


import environ
env = environ.Env()
environ.Env.read_env()

urlpatterns = [
    path(env("HQ_MODEL") + "/admin/", admin.site.urls),
    path('admin/clearcache/', include('clearcache.urls')),  # added
    path("", include("imgapp.urls")),
    path('oauth/', include('social_django.urls', namespace='social')),  # added
    # Alternative
    # path('accounts/', include('allauth.urls', namespace='gosocial')),
    # path('api-auth/', include('rest_framework.urls')),
    # path('api-auth/', include('drf_social_oauth2.urls',namespace='drf')),

  
] 
 

#  Serve the static HTML
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 


# Serve the favicon 
urlpatterns += [
    path('favicon.ico', serve, {
            'path': 'favicon.ico',
            'document_root': os.path.join(BASE_DIR, 'static/staticfiles/images/'),
        }
    ),
]

# Optional generate required secret and keys, than use it
# Switch to social login if it is configured - Keep for later
# try:
#     from . import github_settings
#     social_login = 'registration/login_social.html'
#     urlpatterns.insert(0,
#                        path('accounts/login/', auth_views.LoginView.as_view(template_name=social_login))
#                        )
#     print('Using', social_login, 'as the login template')
# except:
#     print('Using registration/login.html as the login template')

