from django.urls import path, include
from .views import *
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from app_backend_api.schema import schema
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
def trigger_error(request):
    division_by_zero = 1 / 0
    # for sentry logging testing.

from django.urls import path, include
 
...

schema_view = get_schema_view(
openapi.Info(
	title="Dummy API",
	default_version='v1',
	description="Dummy description",
	terms_of_service="https://www.google.com/policies/terms/",
	contact=openapi.Contact(email="contact@dummy.local"),
	license=openapi.License(name="BSD License"),
),
public=True,
permission_classes=(permissions.AllowAny,),
)


# hold up 
urlpatterns = [
    path('testing_testing', testing_testing, name='testing_testing'),
    path('export_contacts', export_contacts_json, name='export_contacts'),
    path('admin_category', admin_category, name='admin_category'),
    path('update_api', update_api, name='update_api'),
    path('contact_api', contact_api_data, name='contact_api'),
    path('all_contact', all_contact_api_data, name='all_contact'),
    path('admin_edit_user', admin_edit_user, name='admin_edit_user'),
    path('admin_delete_user', admin_delete_user, name='admin_delete_user'),
    path('view_user', view_user, name='view_user'),
    path('category_api', category_api_data, name='category_api'),
    path('outreach_api', outreach_api_data, name='outreach_api'),
    path('contact_email_api', contact_email_api_data, name='contact_email_api'),
    path('category_email_api', category_email_api_data, name='category_email_api'),
    path('minister_email_api', minister_email_api_data, name='minister_email_api'),
    path('register_api', register_api_data, name='register_api'),
    path('outreach_registration_api', outreach_registration_api_data, name='outreach_registration_api'),
    path('create_account', create_account, name='create_account'),
    path('analyticals', analytic_report, name='analytics'),
    path('token_validation', token_validation, name='token_validation'),
    path('user_profile', user_profile, name='user_profile'),
    path('jot_form_api_call', jot_form_api_call, name='jot_form_api_call'),
    path('text_confirmation', text_confirmation, name='text_confirmation'),
    path('all_outreach', all_outreach, name='all_outreach'),
    path('view_recipient', view_recipient, name='view_recipient'),
    path('image_kit_api', image_kit_api, name='image_kit_api'),
    path('outreach_contact_email_api_data', outreach_contact_email_api_data, name='outreach_contact_email_api_data'),
    path('login_verification', CustomAuthToken.as_view(), name='login_verification'),  # <-- And here
    # change to your custom view
    path('accounts/', include('django.contrib.auth.urls')),
    path('sentry_debug/', trigger_error),
    # for sentry testing
    path('__debug__/', include('debug_toolbar.urls')),
    # for debug of django
    # ONLY FOR TESTING.
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    # graphing
    path("docs/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


]