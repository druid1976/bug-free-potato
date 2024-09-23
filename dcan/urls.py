"""
URL configuration for dcan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.http import HttpResponseRedirect
from django.urls import path, include, reverse
from django.conf.urls.static import static

from dcan import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: HttpResponseRedirect(reverse("accounts:blank"))),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('course/', include(('courses.urls', 'courses'), namespace='courses')),
    path('questionaire/', include(('qa.urls', 'qa'), namespace='qa')),
    path('backrooms/', include('chatroom.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

