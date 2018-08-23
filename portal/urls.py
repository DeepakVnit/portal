from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from portalapp import views as appview
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    url(r'^register/?$', appview.RegistrationAPIView.as_view(), name='register'),
    url(r'^user/?$', appview.UserRetrieveUpdateAPIView.as_view(), name='user'),
    url(r'^login/$', appview.LoginAPIView.as_view(), name='login'),
    url(r'^profile/?$', appview.ProfileRetrieveAPIView.as_view()),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
