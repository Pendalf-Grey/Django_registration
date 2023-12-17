from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import views, profile


schema_view = get_schema_view(
    openapi.Info(
        title="Registration API",
        default_version='v1',
        description="API for user registration",
        terms_of_service="http://www.it-shag.com/terms/",
        contact=openapi.Contact(email="contact@gmail.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('register/', views.registration_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/create/', profile.create_profile, name='create_profile'),
    path('profile/', profile.view_profile, name='view_profile'),
    path('profile/update/', profile.update_profile, name='update_profile'),
    path('profile/delete/', profile.delete_profile, name='delete_profile'),
]


