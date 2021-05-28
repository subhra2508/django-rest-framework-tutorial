from django.contrib import admin
from django.urls import path, include
from restapi.views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from restapi.auth import CustomAuthToken

# Creating router object
router = DefaultRouter()

# Register StudentViewSet with Router
# router.register('studentapi', StudentViewSet, basename='student')
router.register('studentapi', StudentModelViewSet, basename='student')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('stucreate/', student_create),

    # function based api views
    # path('studentapi/', student_api),
    # path('studentapi/<str:pk>/', student_api),

    # classBased api views
    # path('studentapi/', StudentAPI.as_view()),
    # path('studentapi/<str:pk>/', StudentAPI.as_view()),

    # using genericviews and mixin
    # path('studentapi/', StudentList.as_view()),
    # path('studentapi/', StudentCreate.as_view()),
    # path('studentapi/<str:pk>/', StudentRetrive.as_view()),
    # path('studentapi/<str:pk>/', StudentUpdate.as_view()),
    # path('studentapi/<str:pk>/', StudentDestroy.as_view()),
    # path('studentapi/', LCStudentAPI.as_view()),
    # path('studentapi/<str:pk>/', RUDStudentAPI.as_view()),

    # USING ROUTERS
    path('', include(router.urls)),
    # adding token drf-token url
    # path('gettoken/', obtain_auth_token),
    # path('gettoken/', CustomAuthToken.as_view()),

    # SIMPLE JWT PATH
    path('gettoken/', TokenObtainPairView.as_view()),
    path('refreshtoken/', TokenRefreshView.as_view()),
    path('verifytoken/', TokenVerifyView.as_view()),

]
#  path('stuinfo/<str:pk>/', student_details),
#  path('stuinfo/', student_list),
