from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from sociallogin.views import Home

schema_view = get_swagger_view(title='SWAGGER APIS')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('useraccount.urls')),
    path('schema/', schema_view),
    path('', Home.as_view(), name='home'),
    path('home/', Home.as_view(), name='home'),
    path('api/', include('sociallogin.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/', include('notes.urls'))

]
