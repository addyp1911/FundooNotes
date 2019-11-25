from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from sociallogin.views import Home

# from notes.urls import router

schema_view = get_swagger_view(title='SWAGGER APIS')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('useraccount.urls')),
    path('schema/', schema_view),
    path('', Home.as_view(), name='home'),
    path('home/', Home.as_view(), name='home'),
    path('api/', include('sociallogin.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/', include('notes.urls')),
    # path('search/', include(router.urls)),

]
