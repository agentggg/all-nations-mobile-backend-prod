from celery import shared_task
# from django.core.mail import send_mail
from app_backend.settings import EMAIL_HOST_USER
import os
from django.core.mail import send_mail
from datetime import timedelta, datetime
from datetime import date
import json
from .models import *
from twilio.rest import Client 
import environ
# Initialise environment variables.
env = environ.Env()
environ.Env.read_env()
from django.core.management import call_command
from io import StringIO
import sys
from datetime import datetime
import cloudinary
import cloudinary.uploader
from imagekitio import ImageKit

contact_admin = env("EMAIL_HOST_USER")
email = env("EMAIL_HOST_USER")
pas = env("EMAIL_HOST_PASSWORD")
imagekit = ImageKit(
    private_key=("PRIVATE_KEY_IMAGE"),
    public_key=("PUBLIC_KEY_IMAGE"),
    url_endpoint=("URL_ENDPOINT_IMAGE")
)

@shared_task
def createNewAccountSendEmailApproval(email_subject, email_message, email_host, email_recipient):
    send_mail(email_subject, email_message, email_host, [email_recipient])  
    return("email task has been sent")

@shared_task
def send_outreach_contact_text(frontendContactArrayType, frontendMessageTask, frontendUserId, frontEndOrg):
    confirmedMessagesSent = {}
    if len(frontendContactArrayType) == 1:
        # checks if the array index count is 1... if it is more then 1, then it skips this section and then loops
        frontendContact = ' '.join(frontendContactArrayType)
        # converts the frontendContactArrayType into a string to be accessible in the code as a string
        numberQuery = OutreachRegistrationForm.objects.filter(outreach_first_name=frontendContact).values_list('outreach_phone_number', flat=True).first()
        # retrieve phone number value from database in QuerySet format <QuerySet ['6786820502', '6786820502']>
        TWILIO_ACCOUNT_SID = OrganizationAccount.objects.get(org_name=frontEndOrg).org_sid
        TWILIO_ACCOUNT_TOKEN = OrganizationAccount.objects.get(org_name=frontEndOrg).org_token
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
        client.messages.create(body=frontendMessageTask, to=[numberQuery], from_="4704678410")
        confirmedMessagesSent[frontendContact] = numberQuery
        # updates dictionary for text confirmation
    else:
      for frontendContactItems in frontendContactArrayType:
        # loops through the categroy array ['RAW', 'Equipping Session']
        numberQuery = OutreachRegistrationForm.objects.filter(outreach_first_name=frontendContactItems).values_list('outreach_phone_number', flat=True).first()
        # retrieve phone number value from database in QuerySet format <QuerySet ['6786820502', '6786820502']>
        TWILIO_ACCOUNT_SID = OrganizationAccount.objects.get(org_name=frontEndOrg).org_sid
        TWILIO_ACCOUNT_TOKEN = OrganizationAccount.objects.get(org_name=frontEndOrg).org_token
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
        client.messages.create(body=frontendMessageTask, to=[numberQuery], from_="4704678410")
        # confirmedMessagesSent.update({frontendContactItems : numberQuery})
        confirmedMessagesSent[frontendContactItems] = numberQuery
    user_email_from_database = CustomUser.objects.filter(id=frontendUserId).values_list('email', flat=False)
    user_email_from_database_plain_text = json.dumps(list(user_email_from_database)[0][0]).replace('"','')
    confirmationEmail = (f"""The following users were sent the following message. Thank you for using Go All Nations:

Recipients: {confirmedMessagesSent}

Message that was sent: {frontendMessageTask}

Jesus said to him, “Rise, take up your bed and walk.” 

Evolving Technologies LLC
""")
    # text message that will be sent
    send_mail("Confirmed Text Sent", confirmationEmail, EMAIL_HOST_USER, [user_email_from_database_plain_text])
    # sends confirmation email to the admin
    return (f"Message sent successfully to {confirmedMessagesSent}")

@shared_task
def send_contact_text(frontendContactArrayType, frontendMessageTask, frontendUserId, frontEndOrg):
    confirmedMessagesSent = {}
    if len(frontendContactArrayType) == 1:
        # checks if the array index count is 1. if it is more then 1, then it skips this section and then loops
        frontendContact = ' '.join(frontendContactArrayType)
        # converts the frontendContactArrayType into a string to be accessible in the code as a string
        numberQuery = Contact.objects.filter(first_name_info=frontendContact).values_list('phone_number_info', flat=True).first()
        # retrieve phone number value from database in QuerySet format <QuerySet ['6786820502', '6786820502']>
        TWILIO_ACCOUNT_SID = OrganizationAccount.objects.get(org_name=frontEndOrg).org_sid
        TWILIO_ACCOUNT_TOKEN = OrganizationAccount.objects.get(org_name=frontEndOrg).org_token
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
        client.messages.create(body=frontendMessageTask, to=[numberQuery], from_="4704678410")
        confirmedMessagesSent[frontendContact] = numberQuery
        # updates dictionary for text confirmation
    else:
      for frontendContactItems in frontendContactArrayType:
        # loops through the categroy array ['RAW', 'Equipping Session']
        numberQuery = Contact.objects.filter(first_name_info=frontendContactItems).values_list('phone_number_info', flat=True).first()
        # retrieve phone number value from database in QuerySet format <QuerySet ['6786820502', '6786820502']>
        TWILIO_ACCOUNT_SID = OrganizationAccount.objects.get(org_name=frontEndOrg).org_sid
        TWILIO_ACCOUNT_TOKEN = OrganizationAccount.objects.get(org_name=frontEndOrg).org_token
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
        client.messages.create(body=frontendMessageTask, to=[numberQuery], from_="4704678410")
        # confirmedMessagesSent.update({frontendContactItems : numberQuery})
        confirmedMessagesSent[frontendContactItems] = numberQuery
    user_email_from_database = CustomUser.objects.filter(id=frontendUserId).values_list('email', flat=False)
    user_email_from_database_plain_text = json.dumps(list(user_email_from_database)[0][0]).replace('"','')
    confirmationEmail = (f"""The following users were sent the following message. Thank you for using Go All Nations:
Recipients: {confirmedMessagesSent}
Message that was sent: {frontendMessageTask}
Jesus said to him, “Rise, take up your bed and walk.” 
Evolving Technologies LLC
""")
    # text message that will be sent
    send_mail("Confirmed Text Sent", confirmationEmail, EMAIL_HOST_USER, [user_email_from_database_plain_text])
    # sends confirmation email to the admin
    return (f"Message sent successfully to {confirmedMessagesSent}")

@shared_task
def send_category_text(frontendContactArrayType, frontendMessageTask, frontendUserId, frontEndOrg):
    confirmedMessagesSent = {}
    # dictionary that maps category names to category number
    if len(frontendContactArrayType) == 1:
        # checks if the array index count is 1. if it is more then 1, then it skips this section and then loops
        frontendCategory = ' '.join(frontendContactArrayType)
        # converts the frontendContactArrayType into a string to be accessible in the code as a string
        category_value = CategoryGroup.objects.values_list('id', flat=True).get(org=frontEndOrg, name_info=frontendCategory)
        # this will convert the category name into category id number to be able to build the relational table
        categroyQuery = Contact.objects.filter(contact_category_id=category_value).values_list('phone_number_info', flat=True)
        #stdout a list of numbers in QuerySet format from the category
        for eachNumber in categroyQuery:
            # stdout each number in the QuerySet individually
            nameQuery = Contact.objects.filter(phone_number_info=eachNumber).values_list('first_name_info', flat=True).first()
            # stdout number for each name
            confirmedMessagesSent[nameQuery] = eachNumber
            # creates a dictionary of strings for confirmation email that will be sent
            TWILIO_ACCOUNT_SID = OrganizationAccount.objects.get(org_name=frontEndOrg).org_sid
            TWILIO_ACCOUNT_TOKEN = OrganizationAccount.objects.get(org_name=frontEndOrg).org_token
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
            client.messages.create(body=frontendMessageTask, to=[eachNumber], from_="4704678410")
            confirmedMessagesSent[nameQuery] = eachNumber
            # creates a dictionary of strings for confirmation email that will be sent
    else:
        for eachCategroy in frontendContactArrayType:
            # loops through the the category selections from frontend
            category_value = CategoryGroup.objects.values_list('id', flat=True).get(org=frontEndOrg, name_info=eachCategroy)
            # this will convert the category name into category id number to be able to build the relational table
            categroyQuery = Contact.objects.filter(contact_category_id=category_value).values_list('phone_number_info', flat=True)
            #stdout a list of numbers in QuerySet format from the category
            for eachNumber in categroyQuery:
                # stdout each number in the QuerySet individually
                nameQuery = Contact.objects.filter(phone_number_info=eachNumber).values_list('first_name_info', flat=True).first()
                # stdout number for each name
                confirmedMessagesSent[nameQuery] = eachNumber
                # creates a dictionary of strings for confirmation email that will be sent
                TWILIO_ACCOUNT_SID = OrganizationAccount.objects.get(org_name=frontEndOrg).org_sid
                TWILIO_ACCOUNT_TOKEN = OrganizationAccount.objects.get(org_name=frontEndOrg).org_token
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
                client.messages.create(body=frontendMessageTask, to=[eachNumber], from_="4704678410")
                confirmedMessagesSent[nameQuery] = eachNumber
                # creates a dictionary of strings for confirmation email that will be sent
    user_email_from_database = CustomUser.objects.filter(id=frontendUserId).values_list('email', flat=False)
    user_email_from_database_plain_text = json.dumps(list(user_email_from_database)[0][0]).replace('"','')
    confirmationEmail = f"""The following users were sent the following message. Thank you for using Go All Nations:
Recipients: {confirmedMessagesSent}
Message that was sent: {frontendMessageTask}
Jesus said to him, “Rise, take up your bed and walk.” 
Evolving Technologies LLC
"""

    send_mail("Confirmed Text Sent", confirmationEmail, EMAIL_HOST_USER, [user_email_from_database_plain_text])

    return f"Message sent successfully to {confirmedMessagesSent}"

@shared_task
def send_outreach_text(frontendContactArrayType, frontendMessageTask, frontendUserId, frontEndOrg):
    confirmedMessagesSent = {}
    frontendMinister = ' '.join(frontendContactArrayType)
    # converts the frontendContactArrayType into a string to be accessible in the code as a string
    numberQuery = OutreachRegistrationForm.objects.filter(minister_category=frontendMinister).values_list('outreach_phone_number', flat=True)
    #stdout a list of numbers in QuerySet format that matches the minister categroy
    for eachNumber in numberQuery:
        # stdout each number in the QuerySet individually
        nameQuery = OutreachRegistrationForm.objects.filter(outreach_phone_number=eachNumber).values_list('outreach_first_name', flat=True).first()
        # stdout number for each name
        TWILIO_ACCOUNT_SID = OrganizationAccount.objects.get(org_name=frontEndOrg).org_sid
        TWILIO_ACCOUNT_TOKEN = OrganizationAccount.objects.get(org_name=frontEndOrg).org_token
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
        client.messages.create(body=frontendMessageTask, to=[eachNumber], from_="4704678410")
        confirmedMessagesSent[nameQuery] = eachNumber
        # creates a dictionary of strings for confirmation email that will be sent
    user_email_from_database = CustomUser.objects.filter(id=frontendUserId).values_list('email', flat=False)
    user_email_from_database_plain_text = json.dumps(list(user_email_from_database)[0][0]).replace('"','')
    confirmationEmail = (f"""The following users were sent the following message. Thank you for using Go All Nations:
Recipients: {confirmedMessagesSent}
Message that was sent: {frontendMessageTask}
Jesus said to him, “Rise, take up your bed and walk.” 
Evolving Technologies LLC
""")
    # text message that will be sent
    send_mail("Confirmed Text Sent", confirmationEmail, EMAIL_HOST_USER, [user_email_from_database_plain_text])
    # sends confirmation email to the admin
    return (f"Message sent successfully to {confirmedMessagesSent}")



@shared_task
def send_contact_text_image(frontendContactArrayType, frontendMessageTask, frontendUserId, frontEndOrg, file):
    confirmedMessagesSent = {}
    if len(frontendContactArrayType) == 1:
        # checks if the array index count is 1. if it is more then 1, then it skips this section and then loops
        frontendContact = ' '.join(frontendContactArrayType)
        # converts the frontendContactArrayType into a string to be accessible in the code as a string
        numberQuery = Contact.objects.filter(first_name_info=frontendContact).values_list('phone_number_info', flat=True).first()
        # retrieve phone number value from database in QuerySet format <QuerySet ['6786820502', '6786820502']>
        TWILIO_ACCOUNT_SID = OrganizationAccount.objects.get(org_name=frontEndOrg).org_sid
        TWILIO_ACCOUNT_TOKEN = OrganizationAccount.objects.get(org_name=frontEndOrg).org_token
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
        client.messages.create(body=frontendMessageTask, to=[numberQuery], from_="4704678410", media_url=[file])
        confirmedMessagesSent[frontendContact] = numberQuery
        # updates dictionary for text confirmation
    else:
      for frontendContactItems in frontendContactArrayType:
        # loops through the categroy array ['RAW', 'Equipping Session']
        numberQuery = Contact.objects.filter(first_name_info=frontendContactItems).values_list('phone_number_info', flat=True).first()
        # retrieve phone number value from database in QuerySet format <QuerySet ['6786820502', '6786820502']>
        TWILIO_ACCOUNT_SID = OrganizationAccount.objects.get(org_name=frontEndOrg).org_sid
        TWILIO_ACCOUNT_TOKEN = OrganizationAccount.objects.get(org_name=frontEndOrg).org_token
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
        client.messages.create(body=frontendMessageTask, to=[numberQuery], from_="4704678410", media_url=[file])
        # confirmedMessagesSent.update({frontendContactItems : numberQuery})
        confirmedMessagesSent[frontendContactItems] = numberQuery
    user_email_from_database = CustomUser.objects.filter(id=frontendUserId).values_list('email', flat=False)
    user_email_from_database_plain_text = json.dumps(list(user_email_from_database)[0][0]).replace('"','')
    confirmationEmail = (f"""The following users were sent the following message. Thank you for using Go All Nations:

Recipients: {confirmedMessagesSent}

Message that was sent: {frontendMessageTask}

Jesus said to him, “Rise, take up your bed and walk.” 

Evolving Technologies LLC
""")
    # text message that will be sent
    send_mail("Confirmed Text Sent", confirmationEmail, EMAIL_HOST_USER, [user_email_from_database_plain_text])
    # sends confirmation email to the admin
    return (f"Message sent successfully to {confirmedMessagesSent}")

@shared_task
def send_category_text_image(frontendContactArrayType, frontendMessageTask, frontendUserId, frontEndOrg, file):
    confirmedMessagesSent = {}
    # dictionary that maps category names to category number
    if len(frontendContactArrayType) == 1:
        # checks if the array index count is 1. if it is more then 1, then it skips this section and then loops
        frontendCategory = ' '.join(frontendContactArrayType)
        # converts the frontendContactArrayType into a string to be accessible in the code as a string
        category_value = CategoryGroup.objects.values_list('id', flat=True).get(org=frontEndOrg, name_info=frontendCategory)
        # this will convert the category name into category id number to be able to build the relational table
        categroyQuery = Contact.objects.filter(contact_category_id=category_value).values_list('phone_number_info', flat=True)
        #stdout a list of numbers in QuerySet format from the category
        for eachNumber in categroyQuery:
            # stdout each number in the QuerySet individually
            nameQuery = Contact.objects.filter(phone_number_info=eachNumber).values_list('first_name_info', flat=True).first()
            # stdout number for each name
            confirmedMessagesSent[nameQuery] = eachNumber
            # creates a dictionary of strings for confirmation email that will be sent
            TWILIO_ACCOUNT_SID = OrganizationAccount.objects.get(org_name=frontEndOrg).org_sid
            TWILIO_ACCOUNT_TOKEN = OrganizationAccount.objects.get(org_name=frontEndOrg).org_token
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
            client.messages.create(body=frontendMessageTask, to=[eachNumber], from_="4704678410", media_url=[file])
            confirmedMessagesSent[nameQuery] = eachNumber
            # creates a dictionary of strings for confirmation email that will be sent
    else:
        for eachCategroy in frontendContactArrayType:
            # loops through the the category selections from frontend
            category_value = CategoryGroup.objects.values_list('id', flat=True).get(org=frontEndOrg, name_info=eachCategroy)
            # this will convert the category name into category id number to be able to build the relational table
            categroyQuery = Contact.objects.filter(contact_category_id=category_value).values_list('phone_number_info', flat=True)
            #stdout a list of numbers in QuerySet format from the category
            for eachNumber in categroyQuery:
                # stdout each number in the QuerySet individually
                nameQuery = Contact.objects.filter(phone_number_info=eachNumber).values_list('first_name_info', flat=True).first()
                # stdout number for each name
                confirmedMessagesSent[nameQuery] = eachNumber
                # creates a dictionary of strings for confirmation email that will be sent
                TWILIO_ACCOUNT_SID = OrganizationAccount.objects.get(org_name=frontEndOrg).org_sid
                TWILIO_ACCOUNT_TOKEN = OrganizationAccount.objects.get(org_name=frontEndOrg).org_token
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
                client.messages.create(body=frontendMessageTask, to=[eachNumber], from_="4704678410", media_url=[upload_result['secure_url']])
                confirmedMessagesSent[nameQuery] = eachNumber
                # creates a dictionary of strings for confirmation email that will be sent
    user_email_from_database = CustomUser.objects.filter(id=frontendUserId).values_list('email', flat=False)
    user_email_from_database_plain_text = json.dumps(list(user_email_from_database)[0][0]).replace('"','')
    confirmationEmail = f"""The following users were sent the following message. Thank you for using Go All Nations:

Recipients: {confirmedMessagesSent}

Message that was sent: {frontendMessageTask}

Jesus said to him, “Rise, take up your bed and walk.” 

Evolving Technologies LLC
"""

    send_mail("Confirmed Text Sent", confirmationEmail, EMAIL_HOST_USER, [user_email_from_database_plain_text])

    return f"Message sent successfully to {confirmedMessagesSent}"

@shared_task
def send_outreach_text_image(frontendContactArrayType, frontendMessageTask, frontendUserId, frontEndOrg, file):
    confirmedMessagesSent = {}
    frontendMinister = ' '.join(frontendContactArrayType)
    # converts the frontendContactArrayType into a string to be accessible in the code as a string
    numberQuery = OutreachRegistrationForm.objects.filter(minister_category=frontendMinister).values_list('outreach_phone_number', flat=True)
    #stdout a list of numbers in QuerySet format that matches the minister categroy
    for eachNumber in numberQuery:
        # stdout each number in the QuerySet individually
        nameQuery = OutreachRegistrationForm.objects.filter(outreach_phone_number=eachNumber).values_list('outreach_first_name', flat=True).first()
        # stdout number for each name
        TWILIO_ACCOUNT_SID = OrganizationAccount.objects.get(org_name=frontEndOrg).org_sid
        TWILIO_ACCOUNT_TOKEN = OrganizationAccount.objects.get(org_name=frontEndOrg).org_token
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
        client.messages.create(body=frontendMessageTask, to=[eachNumber], from_="4704678410", media_url=[file])
        confirmedMessagesSent[nameQuery] = eachNumber
        # creates a dictionary of strings for confirmation email that will be sent
    user_email_from_database = CustomUser.objects.filter(id=frontendUserId).values_list('email', flat=False)
    user_email_from_database_plain_text = json.dumps(list(user_email_from_database)[0][0]).replace('"','')
    confirmationEmail = (f"""The following users were sent the following message. Thank you for using Go All Nations:

Recipients: {confirmedMessagesSent}

Message that was sent: {frontendMessageTask}

Jesus said to him, “Rise, take up your bed and walk.” 

Evolving Technologies LLC
""")
    # text message that will be sent
    send_mail("Confirmed Text Sent", confirmationEmail, EMAIL_HOST_USER, [user_email_from_database_plain_text])
    # sends confirmation email to the admin
    return (f"Message sent successfully to {confirmedMessagesSent}")



@shared_task
def send_outreach_first_follow_up_email():
    confirmedMessagesSent = {}
    myCurrentdate = date.today()
    # prints 2022-08-24
    myCurrentDatetime = datetime(myCurrentdate.year, myCurrentdate.month, myCurrentdate.day)
    # need this in order to convert time to datetime.datetime
    # futureCheckDay = myCurrentDatetime + timedelta(days=3)
    # futureCheckHour = myCurrentDatetime + timedelta(hours=24)
    # futureCheckMinute = myCurrentDatetime + timedelta(minutes=60)
    # define time delta which will be substracted from the actual time !NOT BEING USED YET WILL BE USED IN FUTURE RELEASE FOR SPECIFIC TIME OF RELEASE!
    allDatabase = OutreachRegistrationForm.objects.values_list('id')
    for allDatabaseItemized in allDatabase:
        stringFormat = str((allDatabaseItemized[0]))
        databaseDay = OutreachRegistrationForm.objects.filter(id=stringFormat).values_list('outreach_date')
        databaseName = OutreachRegistrationForm.objects.filter(id=stringFormat).values_list('outreach_first_name')
        databaseNumber = OutreachRegistrationForm.objects.filter(id=stringFormat).values_list('outreach_phone_number')
        databaseOutreachCategory = OutreachRegistrationForm.objects.filter(id=stringFormat).values_list('outreach_category')
        databaseMinisterCategory = OutreachRegistrationForm.objects.filter(id=stringFormat).values_list('minister_category')
        databaseOutreachSpot = OutreachRegistrationForm.objects.filter(id=stringFormat).values_list('outreach_spot')
        orgName = OutreachRegistrationForm.objects.filter(id=stringFormat).values_list('org_name')
        # extract from database
        databaseNameString =  json.dumps(list(databaseName)[0][0]).replace('"','')
        databaseOutreachCategoryString = json.dumps(list(databaseOutreachCategory)[0][0]).replace('"','')
        databaseMinisterCategoryString = json.dumps(list(databaseMinisterCategory)[0][0]).replace('"','')
        databaseOutreachSpotString =  json.dumps(list(databaseOutreachSpot)[0][0]).replace('"','')
        orgNameString = json.dumps(list(orgName)[0][0]).replace('"','')
        website = OrganizationAccount.objects.get(org_name=orgNameString).org_website_link
        # prints it out as follow "Convert" we need to remove the double quotes
        # removes the quotes from the string so it can be parsed for conditional statement. Prints out like this Convert
        # gather all necc data from database
        extractDatabaseDayLevel_1 = (databaseDay[0])
        extractDatabaseDayLevel_2 = extractDatabaseDayLevel_1[0]
        # extracts the value and converts it to string format because the database will present it as a QuerySet
        datetime_date = datetime.strptime(extractDatabaseDayLevel_2, '%m/%d/%Y')
        # format is datetime.datetime
        # converts the string into time format
        previous_date_threshold = myCurrentDatetime - timedelta(days=3)
        previous_date_over_threshold = myCurrentDatetime - timedelta(days=4)
        def TextBody(category_message, category_group):   
            text_data = (f"""Hi {databaseNameString} this is the Rise And Walk Ministry. Not sure if you remember or not, but {databaseMinisterCategoryString} prayed for you at {databaseOutreachSpotString}. The ministry wanted to reach out to thank you for allowing {databaseMinisterCategoryString} the time to {category_group} with you. {category_message}
How have you been since {databaseMinisterCategoryString} prayed with you? Has there been any changes in your life since? 

Connect to our social media platforms. A lot of good content being pushed there.
{website}
""")
            return (text_data)
            # creates the text message that will be sent. This will be passed into another clas function. All the variables are provided in the 
            # other functions and etc.
        def CreateText(send_text_data):
            #need this to create a class that will point to itself for defination purposes
            #assign self to the text_body variable.
            TWILIO_ACCOUNT_SID = OrganizationAccount.objects.get(org_name=orgNameString).org_sid
            TWILIO_ACCOUNT_TOKEN = OrganizationAccount.objects.get(org_name=orgNameString).org_token
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
            client.messages.create(body=send_text_data, to=databaseNumber, from_ = "4704678410")
            return ("text message successfully sent")
        if datetime_date >= previous_date_threshold >= previous_date_over_threshold and datetime_date <= myCurrentDatetime: 
            # future_date_measurements is today's date plus 3 days, including today. So if today is 8/24, this will be inclusive of 8/24-8/27
            # previous_date_over_threshold is today plus 4 days, which should be excluded So if today is 8/24, this will be anything after 8/27
            # requirment: database date needs to be less then or equal to future date +3, but not greater then future date +3, or less then current date
            # dateime_object is the database object time
            confirmedMessagesSent[json.dumps(list(databaseName)[0][0])] = json.dumps(list(databaseNumber)[0][0])
            # converts the JSON query to a string format. A Django ORM request comes in as the following: <QuerySet [('Stevenson2',)]>
            # json.dumps(list(VARIBALE)) converts it to [('Stevenson2',)] a double nested array
            # The [0][0] extracts the value within the double nested array
            if databaseOutreachCategoryString == "Prayer":
                CreateText(TextBody("Hopefully the prayer was impactful and right timing.", "pray"))
            elif databaseOutreachCategoryString == "Healing":
                CreateText(TextBody("Jesus healed you because He loves you and have a purpose for your life. Share your stroy. You are a living testimony.", "pray for healing"))
            elif databaseOutreachCategoryString == "Challange":
                CreateText(TextBody("Give Jesus a try, you won't regret.", "share the 21 day challange"))
            elif databaseOutreachCategoryString == "Prophetic":
                CreateText(TextBody("You received a prophetic word for your life. We don't know you, and you don't know us, but we heard that the prophetic word was spot on.", "share a Word from the Lord with you"))
            elif databaseOutreachCategoryString == "Convert":
                CreateText(TextBody("Welcome to the family! You will NEVER regret this decision. Check out this video. Let me know what you think about it. https://youtu.be/pUfwuvjTSLo", "pray"))
            elif databaseOutreachCategoryString == "All":
                CreateText(TextBody("Wow! God really has a calling over your life. Amazing! Live for Jesus, and you will NEVER regret", "talk and pray"))      
            elif databaseOutreachCategoryString == "Test":
                CreateText(TextBody("I am sendning a test message", "test this"))
        confirmationEmail = (f"""The following users were sent the following message.

Date: Contacts from {previous_date_threshold} up to {myCurrentdate}, including {myCurrentdate}.

Recipients: 

{confirmedMessagesSent}



Thank you for using Go All Nations. Jesus said to him, “Rise, take up your bed and walk.” 




Evolving Technologies LLC

        """)
        #sending confirmation email text
    send_mail("Confirmed Outreach Text Sent", confirmationEmail, EMAIL_HOST_USER, [contact_admin])
#sends confirmation email message

@shared_task
def createNewAccount(email_subject, email_message, email_host, email_recipient):
    send_mail(email_subject, email_message, email_host, email_recipient)
    return("email task has been sent")

@shared_task
def celery_test():
    send_mail("Confirmed Outreach Text Sent", "testing celery beat email", EMAIL_HOST_USER, [contact_admin])

@shared_task
def database_backup():
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
    return("Backup and email completed")