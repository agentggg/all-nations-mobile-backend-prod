
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.http import JsonResponse
from .serializers import *
from .models import *
from app_backend.settings import EMAIL_HOST_USER
#for message boxes
#https://ordinarycoders.com/blog/article/django-messages-framework
#https://docs.djangoproject.com/en/3.2/topics/db/queries/
from datetime import datetime, date
# email lib
import json
# used to parse the JSON data from the register form
#https://stackoverflow.com/questions/62068698/credentials-are-required-to-create-a-twilioclient
from .tasks import *
from datetime import datetime
from django.http import Http404
from jotform import *
from django.db.models import F
from imagekitio import ImageKit
import cloudinary
import cloudinary.uploader
env = environ.Env()
environ.Env.read_env()


ADMIN_CONTACT = env("EMAIL_HOST_USER")
email = env("EMAIL_HOST_USER")

@api_view(['GET', 'POST'])
def jot_form_api_call(request):
    jotformAPIClient = JotformAPIClient('791a18fee58fabaa1704cf5ed7d48f2c')
    forms = jotformAPIClient.get_forms(None, 1, None, None)
    latestForm = forms[0]
    latestFormID = latestForm["id"]
    submissions = jotformAPIClient.get_form_submissions(latestFormID)
    return Response(submissions)


@api_view(['GET', 'POST'])
def contact_api_data(request):
    username = request.data.get('username', False)
    userPermission = CustomUser.objects.filter(username=username, groups__name='SendMessage').exists()
    userPermissionAdmin = CustomUser.objects.filter(username=username, groups__name='SendMessage').exists()

    if userPermission == False:
        raise Http404
    # this is for the contact_api url which is called in a few forms
    # this will return a list of user, per org 
    try:
        if request.method == 'POST':
            org = request.data.get('org', False)
            # retrieve data from frontend
            first_name_database_request = Contact.objects.filter(org=org).values_list('first_name_info', flat=True).order_by("first_name_info").distinct()
            # this query is used to retrieve only values pertainent to that org
            return Response(first_name_database_request)
    except Exception as e:
        print(e)
    return Response("Please screenshot and contact your system admin if you are seeing this page con-api.")

@api_view(['GET', 'POST'])
def category_api_data(request):
    username = request.data.get('username', False)
    view = request.data.get('pageName', False)
    userPermission = CustomUser.objects.filter(username=username, groups__name='SendMessage').exists()
    if view == 'register':
        userPermissionCategory = CustomUser.objects.filter(username=username, groups__name='RegisterOnly').exists()
        if userPermissionCategory == False:
            raise Http404
        try:
            if request.method == 'POST':
                org = request.data.get('org', False)
                # retrieve data from frontend
                category_name_database_request = CategoryGroup.objects.filter(org=org).values_list('name_info', flat=True)
                # this query is used to retrieve only values pertainent to that username
                return Response(category_name_database_request)
        except Exception as e:
            print(e)
        return Response("Please screenshot and contact your system admin if you are seeing this page. cat-api")

    elif view == 'admin':
        userAdmin = CustomUser.objects.filter(username=username, groups__name='OrgAdmin').exists()
        if userAdmin == False:
            print("No access")
            raise Http404
        try:
            if request.method == 'POST':
                org = request.data.get('org', False)
                # retrieve data from frontend
                category_name_database_request = CategoryGroup.objects.filter(org=org).values_list('name_info', flat=True)
                # this query is used to retrieve only values pertainent to that username
                return Response(category_name_database_request)
        except Exception as e:
            print(e)
        return Response("Please screenshot and contact your system admin if you are seeing this page. cat-api")

    elif userPermission == False:
        print("No access")
        raise Http404
    try:
        if request.method == 'POST':
            org = request.data.get('org', False)
            # retrieve data from frontend
            category_name_database_request = CategoryGroup.objects.filter(org=org).values_list('name_info', flat=True)
            # this query is used to retrieve only values pertainent to that username
            return Response(category_name_database_request)
    except Exception as e:
        print(e)
    return Response("Please screenshot and contact your system admin if you are seeing this page. cat-api")

@api_view(['GET', 'POST'])
def outreach_api_data(request):
    username = request.data.get('username', False)
    userPermission = CustomUser.objects.filter(username=username, groups__name='SendMessage').exists()
    if userPermission == False:
        raise Http404
    # api endpoint for all outreach contacts to become visible
    try:   
        if request.method == 'POST':
            org = request.data.get('org', False)
            # retrieve data from frontend
            minister_name_database_request = OutreachRegistrationForm.objects.filter(org_name=org).values_list('minister_category', flat=True).order_by("minister_category").distinct()
            # this query is used to retrieve only values pertainent to that username
            return Response(minister_name_database_request)
    except Exception as e:
        print(e)
    return Response("Please screenshot and contact your system admin if you are seeing this page out-api")


@api_view(['GET', 'POST'])
def contact_email_api_data(request):
    try:
        if request.method == "POST":
            file = request.data.get('file', False)
            user_username = request.data.get('username', False)
            user_message = request.data.get('message', False)
            user_contact_dictionary = request.data.get('contactSelection', False)
            user_contact = user_contact_dictionary['contact']
            org = request.data.get('org', False)
            # extract the recipient value from frontend. This data is received as a nested array within a dictionary.
            # extract the text message from frontend. Will come in string format
            username_id_database_request = CustomUser.objects.filter(username=user_username).values_list('id', flat=True)
            # retrieving the username info from frontend and accessing the id number value so we can leverage it in the following SQL request
            username_database_request_integer_format = json.dumps(list(username_id_database_request)[0]).replace('"','')
            # converting the username_id_database_request from <QuerySet [1]> to just the number 1
            if file == False:
                send_contact_text.delay(user_contact, user_message, username_database_request_integer_format, org)
            else:
                send_contact_text_image.delay(user_contact, user_message, username_database_request_integer_format, org, file)
            # runs the job in celery backend
            return Response("text sent for processing")
        elif request.method == "GET":
            return Response("Please screenshot and contact your system admin if you are seeing this page 'GET-email-api'")
    except Exception as e:
        return Response(e)
    return Response("Please screenshot and contact your system admin if you are seeing this page con email-api")

@api_view(['GET', 'POST'])
def category_email_api_data(request):
    try:
        if request.method == "POST":
            file = request.data.get('file', False)
            user_username = request.data.get('username', False)
            user_message = request.data.get('message', False)
            user_category_dictionary = request.data.get('contactSelection', False)
            org = request.data.get('org', False)
            user_category = user_category_dictionary['contact']
            username_id_database_request = CustomUser.objects.filter(username=user_username).values_list('id', flat=True)
            # extract the recipient value from frontend. This data is received as a nested array within a dictionary.
            # extract the text message from frontend. Will come in string format
            username_id_database_request = CustomUser.objects.filter(username=user_username).values_list('id', flat=True)
            # retrieving the username info from frontend and accessing the id number value so we can leverage it in the following SQL request
            username_database_request_integer_format = json.dumps(list(username_id_database_request)[0]).replace('"','')
            # converting the username_id_database_request from <QuerySet [1]> to just the number 1
            if file == False:
                send_category_text.delay(user_category, user_message, username_database_request_integer_format, org)
            else:
                send_category_text_image.delay(user_category, user_message, username_database_request_integer_format, org, file)
            # runs the job in celery backend
            return Response("text sent for processing")
        elif request.method == "GET":
            return Response("Please screenshot and contact your system admin if you are seeing this page 'GET-email-api'")
    except Exception as e:
        print(e)
    return Response("Please screenshot and contact your system admin if you are seeing this page con email-api")

@api_view(['GET', 'POST'])
def minister_email_api_data(request):
    # sending text message via the minister category section
    try:
        if request.method == "POST":
            file = request.data.get('file', False)
            user_username = request.data.get('username', False)
            user_message = request.data.get('message', False)
            user_minister_dictionary = request.data.get('contactSelection', False)
            org = request.data.get('org', False)
            user_minister = user_minister_dictionary['contact']
            # extract the recipient value from frontend. This data is received as a nested array within a dictionary.
            # extract the text message from frontend. Will come in string format
            username_id_database_request = CustomUser.objects.filter(username=user_username).values_list('id', flat=True)
            # retrieving the username info from frontend and accessing the id number value so we can leverage it in the following SQL request
            username_database_request_integer_format = json.dumps(list(username_id_database_request)[0]).replace('"','')
            # converting the username_id_database_request from <QuerySet [1]> to just the number 1
            if file == False:
                send_outreach_text.delay(user_minister, user_message, username_database_request_integer_format, org)
            # runs the job in celery backend
            else:
                send_outreach_text_image.delay(user_minister, user_message, username_database_request_integer_format, org, file)
            return Response("text sent for processing")
        elif request.method == "GET":
            return Response("Please screenshot and contact your system admin if you are seeing this page 'GET-email-api'")
    except Exception as e:
        print(e)
    return Response("Please screenshot and contact your system admin if you are seeing this page con email-api")

@api_view(['GET', 'POST'])
def outreach_contact_email_api_data(request):
    # will send messages to the individual contacts
    try:
        if request.method == "POST":
            username = request.data.get('username', False)
            message = request.data.get('message', False)
            contactSelection = request.data.get('contactSelection', False)
            org = request.data.get('org', False)
            allContactSelection = contactSelection['contact']
            # extract the recipient value from frontend. This data is received as a nested array within a dictionary.
            # extract the text message from frontend. Will come in string format
            username_id_database_request = CustomUser.objects.filter(username=username).values_list('id', flat=True)
            # retrieving the username info from frontend and accessing the id number value so we can leverage it in the following SQL request
            username_database_request_integer_format = json.dumps(list(username_id_database_request)[0]).replace('"','')
            # converting the username_id_database_request from <QuerySet [1]> to just the number 1. 
            # this will be used to send confirmation email
            send_outreach_contact_text.delay(allContactSelection, message, username_database_request_integer_format, org)
            # runs the job in celery backend
            return Response("text sent for processing")
        elif request.method == "GET":
            return Response("Please screenshot and contact your system admin if you are seeing this page 'GET-email-api'")
    except Exception as e:
        print(e)
    return Response("Please screenshot and contact your system admin if you are seeing this page con email-api")



@api_view(['GET', 'POST'])
def all_contact_api_data(request):
    username = request.data.get('username', False)
    userPermission = CustomUser.objects.filter(username=username, groups__name='OrgAdmin').exists()
    if userPermission == False:
        raise Http404
    try:
        if request.method == 'POST':
            org = request.data.get('org', False)
            # retrieve data from frontend
            user_info_database_request = Contact.objects.select_related('CategoryGroup').annotate(category_name=F('contact_category__name_info')).filter(org=org).values('first_name_info', 'last_name_info', 'org', 'phone_number_info','category_name', 'contact_notes_info', 'id').order_by("category_name")
            return Response(user_info_database_request)
    except Exception as e:
        print(e)
    return Response("Please screenshot and contact your system admin if you are seeing this page con-api.")

@api_view(['GET', 'POST'])
def update_api(request):   
    print('h')
    try:
        if request.method == 'POST':
            firstName = request.data.get('firstName', False)
            lastName = request.data.get('lastName', False)
            notes = request.data.get('notes', False)
            user_profile_pk = request.data.get('id', False)
            outreachCategory = request.data.get('category', False)
            phoneNumber = request.data.get('phone', False)
            org = request.data.get('org', False)
            # retrieve data from FrontEnd
            if firstName != False:
                Contact.objects.filter(id=user_profile_pk).update(first_name_info=firstName)  
            if lastName != False:
                Contact.objects.filter(id=user_profile_pk).update(last_name_info=lastName)  
            if notes != False:
                Contact.objects.filter(id=user_profile_pk).update(contact_notes_info=notes) 
            if outreachCategory != "placeholder":
                CategoryUpdate = CategoryGroup.objects.filter(name_info=outreachCategory, org=org).values_list("id", flat=True)
                Contact.objects.filter(id=user_profile_pk).update(contact_category_id=CategoryUpdate)  
            if phoneNumber != False:
                Contact.objects.filter(id=user_profile_pk).update(phone_number_info=phoneNumber) 
            return Response("Updated all entries successfully")
    except Exception as e:
        print(e)
    return Response("Please screenshot and contact your system admin if you are seeing this page con-api.")

@api_view(['GET', 'POST'])
def admin_delete_user(request):
    try:
        if request.method == 'POST':
            user = request.data.get('user', False)
            # retrieve data from frontend
            Contact.objects.filter(id=user).delete()
            # this query is used to retrieve only category values pertainent to that username
            return Response("Contact deleted")
    except Exception as e:
        print(e)
    return Response("Please screenshot and contact your system admin if you are seeing this page. cat-api")


@api_view(['GET', 'POST'])
def register_api_data(request):
    username = request.data.get('username', False)
    userPermission = CustomUser.objects.filter(username=username, groups__name='RegisterOnly').exists()
    if userPermission == False:
        raise Http404
    # api endpoint to register contacts into the database
    try:       
        if request.method == "POST":
            firstName=request.data.get("firstName", False)
            lastName=request.data.get("lastName", False)
            phoneNumber=request.data.get("phoneNumber", False)
            notes=request.data.get("notes", False)
            categoryUpdate =request.data.get("category", False)
            userName =request.data.get("username", False)
            org =request.data.get("org", False)
            saveOption =request.data.get("saveOption", False)
            # get data from frontend post to APIENDPOINT
            retrieveIdFromDatabase = CustomUser.objects.filter(username=userName).values_list('id', flat=True)
            # # will retrieve the id from the username database that matches the name of the user. Provides in QuerySet
            categoryEntry = CategoryGroup.objects.values_list('id', flat=True).get(org=org, name_info=categoryUpdate)
            # this will convert the category name into category id number to be able to build the relational table
            retrieveIdFromDatabase_string = retrieveIdFromDatabase[0]
            # provides the database value extracted from the object. QuerySet is an object, and need to extract the value from the object
            Contact.objects.create(
                first_name_info=firstName, 
                last_name_info = lastName,
                phone_number_info = phoneNumber,
                contact_category_id = categoryEntry,
                contact_notes_info = notes,
                user_id = retrieveIdFromDatabase_string,
                org = org
                )
            # saves info to the DB
            if saveOption == 'guestUpdate':
                # if there it is a FT guest, it will send them automated text message
                org_gui_name = OrganizationAccount.objects.get(org_name = org).org_gui_name
                URL = OrganizationAccount.objects.get(org_name=org).org_website_link
                TWILIO_ACCOUNT_SID = OrganizationAccount.objects.get(org_name=org).org_sid
                TWILIO_ACCOUNT_TOKEN = OrganizationAccount.objects.get(org_name=org).org_token
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
                message = f"""Hey, {firstName} thank you for coming to {org_gui_name} event today. We will keep you updated and send you a reminder for our future events via this number. Follow us on social media for Godly content and to hear life changing encounters of what God is doing. Again we truly honor your time and sacrafice. Thank you very much😊
            
{URL}
                """
                client.messages.create(body=message, to=phoneNumber, from_="4704678410")
            return Response("info updated to Database")
        elif request.method == "GET":
            return Response("This is a GET and not a POST. Please contact admin")
    except Exception as e:
        print(e) 
    return Response("Please screenshot and contact your system admin if you are seeing this page reg-api")

@api_view(['GET', 'POST'])
def outreach_registration_api_data(request):   
    username = request.data.get('username', False)
    #gathers the profile first name info to save in the DB
    interactionTime = request.data.get('time', False)
    # retrieves time from frontend, time in user local timezone
    userPermission = CustomUser.objects.filter(username=username, groups__name='OutreachOnly').exists()
    if userPermission == False:
        raise Http404
    # outreach page. Creates database entry and then signals for automated text message
    if request.method == "POST":
        email = request.data.get('email', False)
        # retrieve data from frontend
        username_id_database_request = CustomUser.objects.filter(username=username).values_list('id', flat=True)
        # retrieving the username info from frontend and accessing the id number value so we can leverage it in the following SQL request
        username_database_request_integer_format = json.dumps(list(username_id_database_request)[0]).replace('"','')
        # converting the username_id_database_request from <QuerySet [1]> to just the number 1
        TODAY = date.today()
        now = datetime.now()
        firstName = request.data.get("firstName", False)
        lastName = request.data.get("lastName", False)
        phoneNumber = request.data.get("phoneNumber", False)
        notes = request.data.get("notes", False)
        category = request.data.get("category", False)
        outreachSpotEntry = request.data.get("location", False)
        latitude = request.data.get("latitude", False)
        userLongitude = request.data.get("longitude", False)
        org = request.data.get("org", False) 
        saveOption = request.data.get("saveOption", False)
        OutreachRegistrationForm.objects.create(
            outreach_first_name = firstName, 
            outreach_last_name = lastName,
            outreach_phone_number = phoneNumber,
            outreach_category = category,
            minister_category = username,
            # who ministered to them
            contact_notes = notes,
            outreach_date = TODAY.strftime("%m/%d/%Y"),
            outreach_time = interactionTime,
            outreach_spot = outreachSpotEntry,
            outreach_latitude = latitude,
            outreach_longitude = userLongitude,
            user_id = username_database_request_integer_format,
            user_email = email,
            org_name = org
            )
            # the create method also includes a .save method at the end.
        return Response("user profile created")
    elif request.method == "GET":
        return Response("This is a GET and not a POST. Please contact admin")
    else:
        return Response("Please screenshot and contact your system admin if you are seeing this page")


@api_view(['POST'])
def view_recipient(request):
    username = request.data.get('username', False)
    groupType = request.data.get('groupType', False)
    userPermission = CustomUser.objects.filter(username=username, groups__name='SendMessage').exists()
    if userPermission == False:
        raise Http404
    try:
        if groupType == "category_api":
            contactType = request.data.get('contactType', False)
            org = request.data.get('org', False)
            # extract the recipient value from frontend. This data is received as a nested array within a dictionary.
            # extract the text message from frontend. Will come in string format
            username_id_database_request = CustomUser.objects.filter(username=username).values_list('id', flat=True)
            # retrieving the username info from frontend and accessing the id number value so we can leverage it in the following SQL request
            username_database_request_integer_format = json.dumps(list(username_id_database_request)[0]).replace('"','')
            if len(contactType) == 1:
                # checks if the array index count is 1. if it is more then 1, then it skips this section and then loops
                frontendCategory = ' '.join(contactType)
                # converts the minister into a string to be accessible in the code as a string
                category_value = CategoryGroup.objects.values_list('id', flat=True).get(org=org, name_info=frontendCategory)
                # this will convert the category name into category id number to be able to build the relational table
                categroyQuery = Contact.objects.filter(contact_category_id=category_value).values_list('first_name_info', flat=True)
            return Response(categroyQuery)
        elif groupType == "outreach_api":
            contactType = request.data.get('contactType', False)
            org = request.data.get('org', False)
            # extract the recipient value from frontend. This data is received as a nested array within a dictionary.
            # extract the text message from frontend. Will come in string format
            username_id_database_request = CustomUser.objects.filter(username=username).values_list('id', flat=True)
            # retrieving the username info from frontend and accessing the id number value so we can leverage it in the following SQL request
            if len(contactType) == 1:
                # checks if the array index count is 1. if it is more then 1, then it skips this section and then loops
                frontendCategory = ' '.join(contactType)
                # converts the minister into a string to be accessible in the code as a string
                ambassadorContact = OutreachRegistrationForm.objects.filter(minister_category=frontendCategory).values_list('outreach_first_name', flat=True)
                # this will convert the category name into category id number to be able to build the relational table
            return Response(ambassadorContact)
    except Exception as e:
        print(e)
        return Response(e)
    raise Http404


@api_view(['POST'])
def create_account(request):
    try:
        if request.method == "POST":
            name = request.data.get("username", False)
            pword = request.data.get("password", False)
            fname = request.data.get("firstName", False)
            lname = request.data.get("lastName", False)
            email = request.data.get("email", False)
            org = request.data.get("organization", False)
            user = CustomUser.objects.create_user(
                username = name, 
                password = pword, 
                first_name = fname, 
                last_name = lname,
                email = email,
                org = org
                ) 
            user.is_active = False
            user.save()
            # this creates the user and the next one does the token portion using Django built in
            user_profile_email = (f"""            
The following account requires approval. Please visit admin site to approve:

Username: {name}
First name: {fname}
Last name: {lname}
email: {email}
organiztation: {org}
            """)
            user_account_creator_email = (f"""            
The following account has been sent to the All Nations team for approval. 

Please contact your organization admin if your account has not been activated after 72 hours:

Username: {name}
First name: {fname}
Last name: {lname}
email: {email}
            """)
            createNewAccount.delay("Thank you for signing up!", user_account_creator_email, ADMIN_CONTACT, [email])
            # sends email to account creator that request has been sent and approval is pending
            createNewAccount.delay("All Nations Account Approval Needed", user_profile_email, EMAIL_HOST_USER, [contact_admin])
            # sends account notification to admin
            # to be updated. needs to be a click of a link to switch from false is_active to true is_active
            print("job has been sent to que for processing email notification")
        return Response("account created")
    except Exception as e:
        return Response("Please screenshot and contact your system admin if you are seeing this page")

@api_view(['GET', 'POST'])
def token_validation(request):
    if request.method != "POST":
        return Response("This is a POST and not a GET. Please contact admin")
    username_front_frontend = request.data.get("username", False)
    user_identification_value = CustomUser.objects.get(username=username_front_frontend)
    token_value = Token.objects.filter(user_id=user_identification_value).values_list('key', flat=True)
    return Response(token_value)

@api_view(['GET', 'POST'])
def analytic_report(request):
    username = request.data.get('username', False)
    userPermission = CustomUser.objects.filter(username=username, groups__name='OrgAdmin').exists()
    if userPermission == False:
        raise (Http404)
    if request.method == "POST":
        org = request.data.get('org', False)
        # retrieve data from frontend
        outreach_lat_database_request = OutreachRegistrationForm.objects.filter(org_name=org).values_list('outreach_latitude', flat=True)
        outreach_long_database_request = OutreachRegistrationForm.objects.filter(org_name=org).values_list('outreach_longitude', flat=True)
        outreach_first_name = OutreachRegistrationForm.objects.filter(org_name=org).values_list('outreach_first_name', flat=True)
        outreach_category = OutreachRegistrationForm.objects.filter(org_name=org).values_list('outreach_category', flat=True)
        outreach_minister = OutreachRegistrationForm.objects.filter(org_name=org).values_list('minister_category', flat=True)
        outreach_spot = OutreachRegistrationForm.objects.filter(org_name=org).values_list('outreach_spot', flat=True)
        outreach_contact_notes = OutreachRegistrationForm.objects.filter(org_name=org).values_list('contact_notes', flat=True)
        outreach_id = OutreachRegistrationForm.objects.filter(org_name=org).values_list('id', flat=True)
        #retireving coordinates from the DB
        complete_coordinates = []
        # starts as empty array, but will have full coordinates in pair.
        for eachArray in range(len(outreach_lat_database_request)):
            pair = [
                outreach_lat_database_request[eachArray], 
                outreach_long_database_request[eachArray], 
                outreach_first_name[eachArray],
                outreach_spot[eachArray],
                outreach_category[eachArray],
                outreach_minister[eachArray],
                outreach_contact_notes[eachArray],
                outreach_id[eachArray]
                ]
            # info of the user being sent
            complete_coordinates.append(pair)
        return Response(complete_coordinates)


@api_view(['GET', 'POST'])
def view_user(request):
    # username = request.data.get('username', False)
    # userPermission = CustomUser.objects.filter(username=username, groups__name='OrgAdmin').exists()
    # if userPermission == False:
    #     raise Http404
    try:
        if request.method == 'POST':
            org = request.data.get('org', False)
            # retrieve data from frontend
            user_profile = Contact.objects.filter(org=org).all().values()            
            return Response(user_profile)
    except Exception as e:
        print(e)
    return Response("Please screenshot and contact your system admin if you are seeing this page con-api.")

@api_view(['GET', 'POST'])
def admin(request):
    if request.method == "POST":
        user_username = request.data.get('username', False)
        # retrieve data from frontend
        username_id_database_request = CustomUser.objects.filter(username=user_username).values_list('id', flat=True)
        # retrieving the username info from frontend and accessing the id number value so we can leverage it in the following SQL request
        username_database_request_integer_format = json.dumps(list(username_id_database_request)[0]).replace('"','')
        # converting the username_id_database_request from <QuerySet [1]> to just the number 1
        outreach_lat_database_request = OutreachRegistrationForm.objects.filter(user_id=username_database_request_integer_format).values_list('outreach_latitude', flat=True)
        outreach_long_database_request = OutreachRegistrationForm.objects.filter(user_id=username_database_request_integer_format).values_list('outreach_longitude', flat=True)
        #retireving coordinates from the DB
        complete_coordinates = []
        # starts as empty array, but will have full coordinates in pair
        for eachArray in range(len(outreach_lat_database_request)):
            pair = [outreach_lat_database_request[eachArray] , outreach_long_database_request[eachArray]]
            complete_coordinates.append(pair)
        return Response(complete_coordinates)

@api_view(['GET', 'POST'])
def admin_category(request):
    username = request.data.get('username', False)
    userPermission = CustomUser.objects.filter(username=username, groups__name='OrgAdmin').exists()
    if userPermission == False:
        raise Http404
    try:
        if request.method == 'POST':
            contact_id = request.data.get('id', False)            
            # retrieve data from frontend
            contact_name_database_request = Contact.objects.filter(id=contact_id).values_list('contact_category_id', flat=True)
            username_database_request_integer_format = json.dumps(list(contact_name_database_request)[0]).replace('"','')
            category_name_database_request = CategoryGroup.objects.filter(id=username_database_request_integer_format).values_list('name_info', flat=True)
            # this query is used to retrieve only values pertainent to that username
            send_to_frontend = json.dumps(list(category_name_database_request)[0]).replace('"','')
            return Response(send_to_frontend)
    except Exception as e:
        print(e)
    return Response("Please screenshot and contact your system admin if you are seeing this page. cat-api")

@api_view(['GET', 'POST'])
def user_profile(request):
    org = request.data.get('org', False)
    org_youtube_link = OrganizationAccount.objects.get(org_name = org).org_youtube_link
    org_facebook_link = OrganizationAccount.objects.get(org_name = org).org_facebook_link
    org_instagram_link = OrganizationAccount.objects.get(org_name = org).org_instagram_link
    org_tiktk_link = OrganizationAccount.objects.get(org_name = org).org_tiktk_link
    org_gui_name = OrganizationAccount.objects.get(org_name = org).org_gui_name
    return Response({
            'org_youtube_link': org_youtube_link,
            'org_facebook_link': org_facebook_link,
            'org_instagram_link': org_instagram_link,
            'org_tiktk_link': org_tiktk_link,
            'org_gui_name': org_gui_name
    })


@api_view(['GET', 'POST'])
def admin_edit_user(request):
    apiView = request.data.get('view', False)
    username = request.data.get('username', False)
    userPermission = CustomUser.objects.filter(username=username, groups__name='OrgAdmin').exists()
    if userPermission == False:
        raise Http404
    try:
        if request.method == 'POST':
            user_selected_id = request.data.get('user', False)
            # retrieve data from frontend
            if apiView == 'outreach':
                outreach_database_request = OutreachRegistrationForm.objects.filter(id=user_selected_id).all().values().order_by("outreach_date")
                return Response(outreach_database_request)
            else:
                category_name_database_request_name = Contact.objects.select_related('CategoryGroup').annotate(category_name=F('contact_category__name_info')).filter(id=user_selected_id).values('contact_notes_info', 'first_name_info', 'id', 'last_name_info', 'org', 'phone_number_info','category_name')
                # this query is used to retrieve only category values pertainent to that username
                return Response(category_name_database_request_name)
    except Exception as e:
        print(e)
    return Response("Please screenshot and contact your system admin if you are seeing this page. cat-api")


@api_view(['GET', 'POST'])
def export_contacts_json(request): 
    username = request.data.get('username', False)
    userPermission = CustomUser.objects.filter(username=username, groups__name='OrgAdmin').exists()
    if userPermission == False:
        print("No access")
        raise Http404
            # function is used to export all the contacts in the contacts database and then send them over to frontend for excel
            # used with the URL export_contacts, and frontend component of Admin.js
    try:
        if request.method == 'POST':
            data = list(Contact.objects.select_related('CategoryGroup').annotate(category_name=F('contact_category__name_info')).values('first_name_info', 'last_name_info', 'org', 'phone_number_info','category_name', 'contact_notes_info', ))
            return JsonResponse(data, safe=False)  # or JsonResponse({'data': data})
    except Exception as e:
        print(e)
    return Response("Please screenshot and contact your system admin if you are seeing this page. cat-api")

@api_view(['GET', 'POST'])
def text_confirmation(request):
    return Response('test')

@api_view(['GET', 'POST'])
def all_outreach(request):
    username = request.data.get('username', False)
    userPermission = CustomUser.objects.filter(username=username, groups__name='OrgAdmin').exists()
    if userPermission == False:
        raise Http404
    try:
        if request.method == 'POST':
            userView = request.data.get('userView', False)
            org = request.data.get('org', False)
            # retrieve data from frontend
            if userView == 'outreachContacts':
                user_profile = OutreachRegistrationForm.objects.filter(org_name=org).values_list('outreach_first_name', flat=True).order_by("outreach_date")
            else:
                user_profile = OutreachRegistrationForm.objects.filter(org_name=org).values('outreach_first_name', 'outreach_last_name', 'outreach_phone_number', 'outreach_spot','outreach_category', 'outreach_date', 'contact_notes', 'user_id', 'org_name', 'minister_category', 'id').order_by("outreach_date")
            return Response(user_profile)
    except Exception as e:
        print(e)
    return Response("Please screenshot and contact your system admin if you are seeing this page con-api.")



class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
                'token': token.key,
                'name': user.first_name,
                'username':user.username,
                'email':user.email,
                'org':user.org,
                'status':True
            })
        # sent to the frontend

@api_view(['GET', 'POST'])
def image_kit_api(request):
    imagekit = ImageKit(
        public_key='public_aDahP208/A6D0rqkxn5opFd4m6o=',
        private_key='private_Wdi3LTfI9KmRws+U/NZDkQxSdTE=',
        url_endpoint = 'localhost'
    )
    auth_params = imagekit.get_authentication_parameters()
    return Response(auth_params)


@api_view(['GET', 'POST'])
def testing_testing(request):
    old_stdout = sys.stdout
    result = StringIO()
    sys.stdout = result
    call_command('dumpdata')
    sys.stdout = old_stdout
    result_string = result.getvalue()
    now = datetime.now()
    fullDate = now.strftime("%m/%d/%Y")
    emailSubject = f"""All Nations Backup for {fullDate}"""
    send_mail(emailSubject, result_string, EMAIL_HOST_USER, ['gersard@yahoo.com'])
    return Response('backup process completed')
