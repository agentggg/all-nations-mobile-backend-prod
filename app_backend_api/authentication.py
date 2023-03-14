# from rest_framework.authentication import TokenAuthentication
# from app_backend_api.models import auth_token


# class customAuth(TokenAuthentication):
#     model = auth_token



#this auth file subclassed from restframework TokenAuthication 
#We are telling it is this add info into TokenAuth but get it from this model... it comes from our created model in models.py file
#So basically we subclassed the user and token DRF?
#For the user we subclassed it from Django and we added to them we removed nothing 
#The token we subclassed it from DRF and we added to them we removed nothing