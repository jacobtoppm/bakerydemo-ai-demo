from django.views.decorators.cache import never_cache
from wagtail.admin.urls import display_custom_404
from wagtail.admin.auth import require_admin_access
from wagtail.utils.urlpatterns import decorate_urlpatterns
import bakerydemo.workflow.views as views
from django.urls import path


# These urls need to be included with the same path as the admin, to override the standard workflow create and edit views
# we can't use the 'register_admin_urls' hook here as the normal urls will take precedence
urlpatterns = [
    path("workflows/add/", views.CustomCreate.as_view()),
    path("workflows/edit/<int:pk>/", views.CustomEdit.as_view()),
]

# Wrap them with the normal Wagtail admin decorators
urlpatterns = decorate_urlpatterns(urlpatterns, require_admin_access)
urlpatterns = decorate_urlpatterns(urlpatterns, display_custom_404)
urlpatterns = decorate_urlpatterns(urlpatterns, never_cache)
