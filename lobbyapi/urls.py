"""argamato URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
import importlib, sys, os
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings

from rest_framework import routers, viewsets

from django.conf.urls.static import static

from hatvp.views import home

def auto_register_viewsets(router):
    '''
    Automatically register subclasses of rest_framework.viewsets.ModelViewSet
    found in a local app 'views' module.

    To add a new ModelViewSet to the API, follow these steps:
    
    1. Create a file <app>/views/<model>.py

    2. Write a class <model>ViewSet that inherits ModelViewSet

    3. Edit this class to suit your needs

    4. Import the class in <app>/views/__init__.py

        from .<model> import <model>ViewSet

    The viewset route will be '<app>/<model>'

    Example:
    1. contact/views/details.py

    2. AddressViewSet

    4. from .details import AddressViewSet

    The viewset route is 'contact/address'
    '''
    for app in settings.INSTALLED_APPS:
        # look for 'app/views' module, that is an app with a 'view' module
        try:
            views = importlib.import_module("{}.views".format(app))
        except ModuleNotFoundError as e:
            if "{}.views".format(app) in str(e):
                continue
            else:
                raise e

        # check that the app is a local directory (is a django app)
        if os.path.abspath(views.__file__).startswith(settings.BASE_DIR):
            # list attributes of the module
            if hasattr(views, "viewsets"):
                print(views.viewsets)
                for d in views.viewsets:
                    # check if the attribute is a subclass of GenericViewSet
                    if type(d) == type and issubclass(d, viewsets.GenericViewSet):
                        # get the model
                        m = d.serializer_class.Meta.model
                        # build the route and register
                        router.register(
                            "{}/{}".format(m._meta.app_label, m._meta.model_name),
                            d,
                            basename=m._meta.model_name,
                        )

    return router

router = auto_register_viewsets(routers.SimpleRouter())
print(router.urls)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('schema-viewer/', include('schema_viewer.urls')),
    path('', home)
]


#if settings.DEBUG == True:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
