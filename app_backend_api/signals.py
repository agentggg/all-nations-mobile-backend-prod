from app_backend.settings import EMAIL_HOST_USER
import time 
# retrieves email info from backend
from django.contrib.auth.models import User
# imports the model user from the database
from django.db.models.signals import post_save, pre_save
# imports the signal POST_SAVE to be used. there are few options
# https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html
from django.dispatch import receiver
# what signal is expected to recieve 
from .tasks import *
# imports task to be used


@receiver(pre_save, sender=CustomUser)
def update_user(sender, instance, **kwargs):
    # https://medium.com/@singhgautam7/django-signals-master-pre-save-and-post-save-422889b2839
    if instance.id is None:
        # instance is the user information. ID attached to instance is searchning for the user 
        return("no change")
        # will end if no changes. We add this in order to avoid false positive
    previous = CustomUser.objects.get(id=instance.id)
    id_for_user = CustomUser.objects.get(username=previous).id
    if instance.is_active and CustomUser.objects.filter(pk=instance.pk, is_active=False).exists():
        # if post is saved for the User model, then this code is executed/
        updated_user_email = CustomUser.objects.get(id=id_for_user).email
        updated_user_first_name = CustomUser.objects.get(id=id_for_user).first_name
        updated_user_last_name = CustomUser.objects.get(id=id_for_user).last_name
        updated_user_username = CustomUser.objects.get(id=id_for_user).username
        # retrieves the last set of stuff from that was saved in database
        user_profile_email = (f"""            
The following account has been created and is now active:

First name: {updated_user_first_name}
Last name: {updated_user_last_name}
Username: {updated_user_username}
Status: Active

Please visit the following link and login using the credentials that you created

https://www.nations4christ.net/login

John 5:8 "Then Jesus said to him, Rise, take up you bed, and walk.”
        """)
            # message to be sent
        createNewAccountSendEmailApproval.delay("All Nations Account Approved", user_profile_email, EMAIL_HOST_USER, updated_user_email)
        # sends email using the celery function
        return("successfully sent account confirmation email")

@receiver(post_save, sender=OutreachRegistrationForm)
def outreach_initial_text(sender, instance, **kwargs):
    phone_number_entry = OutreachRegistrationForm.objects.latest('id').outreach_phone_number
    phone_number_entry = OutreachRegistrationForm.objects.latest('id').outreach_phone_number
    first_name_entry = OutreachRegistrationForm.objects.latest('id').outreach_first_name
    outreach_category_entry = OutreachRegistrationForm.objects.latest('id').outreach_category
    minister_category_entry = OutreachRegistrationForm.objects.latest('id').minister_category
    outreach_spot_entry = OutreachRegistrationForm.objects.latest('id').outreach_spot
    user_email = OutreachRegistrationForm.objects.latest('id').user_email
    user_org = OutreachRegistrationForm.objects.latest('id').org_name
    TWILIO_ACCOUNT_SID = OrganizationAccount.objects.get(org_name=user_org).org_sid
    TWILIO_ACCOUNT_TOKEN = OrganizationAccount.objects.get(org_name=user_org).org_token
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)

    confirmedMessagesSent = {}
    def TextBody(category_message, category_group):   
        text_data = (f"""Hey there {first_name_entry} this is {minister_category_entry} from {outreach_spot_entry}. {category_message}""")
        return (text_data)
        # creates the text message that will be sent. This will be passed into another clas function. All the variables are provided in the 
        # other functions and etc.

    def CreateText(send_text_data):
        time.sleep(60)
        #need this to create a class that will point to itself for defination purposes
        #assign self to the text_body variable.
        client.messages.create(body=send_text_data, to=phone_number_entry, from_ = "4704678410")
        return ("text message successfully sent")
    confirmedMessagesSent[first_name_entry] = phone_number_entry
    if outreach_category_entry == "Prayer":
        CreateText(TextBody("Hopefully the prayer was impactful and right timing.", "pray"))
    elif outreach_category_entry == "Healing":
        CreateText(TextBody("Today Jesus healed you. He did that because He loves you and have a calling for your life. Share the stroy. Let the world know that Jesus still heals. You are a living testimony.", "pray for healing"))
    elif outreach_category_entry == "Challange":
        CreateText(TextBody("Welcome to the 21 Day challange. Give Jesus a try, you won't regret.", "share the 21 day challange"))
    elif outreach_category_entry == "Prophetic":
        CreateText(TextBody("Today you received a specific word about your life. We don't know you, and you don't know us, but we heard that the prophetic word was spot on.", "share a Word from the Lord with you"))
    elif outreach_category_entry == "Convert":
        CreateText(TextBody("Welcome to the family! You will NEVER regret this decision. Check out this video. Let me know what you think about it. https://youtu.be/pUfwuvjTSLo", "pray"))
    elif outreach_category_entry == "All":
        CreateText(TextBody("Wow! God really has a calling over your life. Amazing! Live for Jesus, and you will NEVER regret", "talk and pray"))      
    elif outreach_category_entry == "Test":
        CreateText(TextBody("I am sendning a test message", "test this"))
    confirmationEmail = (f"""The following users were sent the intial follow-up outreach message.

    Recipients: 

    {confirmedMessagesSent}



    Thank you for using Go All Nations. Jesus said to him, “Rise, take up your bed and walk.” 




    Evolving Technologies LLC
    https://www.evovletech.com 
    

        """)
    #sending confirmation email text
    send_mail("Confirmed Outreach Text Sent", confirmationEmail, EMAIL_HOST_USER, [user_email])
    # sends confirmation email message
    return("public text and confo text sent")