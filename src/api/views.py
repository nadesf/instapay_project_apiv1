from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import status

from api.serializers import UserSigninSerializer, TransactionSerializer, AccountSerializer, ProviderSerializer
from api.serializers import DetailUserSerializer, ListUserTransactionsSerializer, ListUserAccountsSerializer

from api.models import Users, Transactions, Providers, Accounts

# JUSTE POUR LE DEVELOPPEMENT LOCAL
from api.serializers import UserSerializer

# Other Modules
import random
import string 
#import json
import hashlib
import threading 
import time

# Generateur d'identifiant
def userid_generator():
    
    all_chars = string.ascii_letters + string.digits
    identifier = ""

    for i in range(1, 12):
        identifier += random.choice(all_chars)
    
    return identifier

def generate_account_id():

    all_chars = string.ascii_letters + string.digits
    code = ""

    for i in range(1, 12):
        code += random.choice(all_chars)
    
    return code

def transfer_code_generator(send_code=1, receive_code=0):

    all_chars = string.ascii_letters + string.digits

    if send_code:
        code = ""
        for i in range(30):
            code += random.choice(all_chars)
    elif receive_code:
        code = ""
        for i in range(30):
            code += random.choice(all_chars)
    else:
        pass 

    return code

def crypt_password(password):
    
    password_hashed = hashlib.sha256(password.encode()).hexdigest()
    return password_hashed

def generate_transaction_id():

    all_chars = string.ascii_letters + string.digits

    code =  "tran"
    for i in range(10):
        code += random.choice(all_chars)
    return code

def validation_code_transaction():

    all_digits = string.digits
    code = ""

    for i in range(6):
        code += random.choice(all_digits)
       
    return code

def generate_provider_id():

    all_chars = string.ascii_letters + string.digits
    code = "pro"

    for i in range(6):
        code += random.choice(all_chars)
    return code

def control_quality_data(request, data=[]):

    all_punctuation = str(string.punctuation).replace("@", "")
    all_punctuation = all_punctuation.replace(".", "")
    all_punctuation = all_punctuation.replace("-", "")

    for key, value in request.data.items():
        for punctuation in all_punctuation:
            if punctuation in str(value):
                return 0

    if len(data) != 0:
        for var in data:
            for punctuation in all_punctuation:
                if punctuation in var:
                    return 0
    
    return 1

def generate_simple_code():
    all_chars = string.ascii_letters
    code = ""

    for i in range(4):
        code += random.choice(all_chars)
    
    return code


# Déconnecté un utilisateur
def disconnect_user(user_id):
    time.sleep(10)
    queryset = Users.objects.get(pk=user_id)
    queryset.active = False
    queryset.save()

# Create your views here.
def index(request):
    return render(request, "api/index.html")

# Enrégistrer un nouvel utilisateur  SigninUser, LoginUser, ProfilUser
class UserSignin(APIView):

    def post(self, request, *args, **kargs):
        
        # Vérifié les données reçu avant de les utilisés
        checking = control_quality_data(request=request)
        if not checking:
            obj = {
                "Error": "Les données contennient des caractères spéciaux. Veuillez renseigner les champs avec des données valide s'il vous plaît"
            }

            return Response(obj, status=status.HTTP_400_BAD_REQUEST)
            
        # Remplissage des champs restant avant de les envoyés dans le serializer
        request.data['user_id'] = userid_generator()
        request.data['send_code'] = transfer_code_generator()
        request.data['receive_code'] = transfer_code_generator()

        request.data['password'] = crypt_password(request.data['password'])

        with open("beta.txt", "w") as fic:
            fic.write(request.data["password"])

        serializer = UserSigninSerializer(data=request.data)
        if serializer.is_valid():


            with open("beta.txt", "a") as fic:
                fic.write("\n\n")
                fic.write(request.data["password"])
            # Créons automatiquement un compte instapay pour l'utilisateur. Le compte reste désactivé jusqu'à confirmation de l'inscription de l'utilisateur
            serializer.save()
            user = Users.objects.get(pk=request.data['user_id'])
            provider_instapay= Providers.objects.get(provider_name="Instapay")
            Accounts.objects.create(account_id=generate_account_id(), owner=user, provider=provider_instapay, status_account=False)
        
            # On va créer automatiquement un compte instapay pour le nouvel utilisateur
            obj = {
                "success": f"Votre compte à bien été crée",
                "data": [serializer.data]
            }

            return Response(obj, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Authentifié un utilisateur
class UserLogin(APIView):

    def post(self, request, *args, **kargs):

        # Vérifié les données reçus avant de les utilisés
        checking = control_quality_data(request=request)

        if not checking:
            obj = {
                "Error": "Les données contennient des caractères spéciaux. Veuillez renseigner les champs avec des données valide s'il vous plaît"
            }

            return Response(obj, status=status.HTTP_400_BAD_REQUEST)

        try:
        
            # On récupère le contact correspondant depuis la base puis on éffectue la verification
            queryset = Users.objects.get(contact=request.data['contact'])
            password_user = crypt_password(request.data['password'])

            # On vérifie que l'utilisateur ne s'est pas déja connecté sur un autre appareil.
            """
            with open("user_authenticated.txt", "r+") as all_users_connected:
                for user_id in all_users_connected.readlines():
                    if queryset.user_id == user_id:
                        obj = {
                            "Erreur" : "Impossible de vous connectez à se compte !"
                        }
                
                    return Response(obj, status=status.HTTP_401_UNAUTHORIZED)
            """

            if queryset.active == True:
                obj = {
                    "Erreur" : "Impossible de vous connectez à se compte !"
                }
                return Response(obj, status=status.HTTP_401_UNAUTHORIZED)

            if password_user == queryset.password:

                # On va positionner la variable "active" à True
                queryset.active = True
                queryset.save()

                # On récupère la liste des transactions pour ce utilisateur
                user_transaction_send = Transactions.objects.filter(sender=queryset).first()
                user_transaction_receive = Transactions.objects.filter(recipient=queryset).first()

                if user_transaction_send != None and user_transaction_receive != None:
                    user_transactions = user_transaction_send + user_transaction_receive
                    serializer = TransactionSerializer(user_transactions, many=True)
                    list_transactions = serializer.data
                else:
                    list_transactions = []
                

                obj = {
                    "user_id": queryset.user_id,
                    "first_name": queryset.first_name,
                    "last_name": queryset.last_name,
                    "contact": queryset.contact,
                    "send_code": queryset.send_code,
                    "receive_code": queryset.receive_code,
                    "status": queryset.status_user,
                    "name": queryset.name_pointofsale,
                    "location": queryset.location,
                    "transactions": list_transactions
                }

                # Lancement du compte à rebour pour ce user
            
                th1 = threading.Thread(target=disconnect_user, args=(queryset.user_id,))
                th1.start()

                return Response(obj, status=status.HTTP_200_OK)
            else:
                return Response({"Authentication failed": "Mot de passe incorrecte !"}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({"Authentication failed": "Login incorrecte !"}, status=status.HTTP_401_UNAUTHORIZED)


# Editer le profil de l'utilisateur (Changer son mot de passe)
class UserProfile(APIView):

    def post(self, request, *args, **kargs):
        
        # Vérifié les données reçus avant de les utilisés
        checking = control_quality_data(request=request)

        if not checking:
            obj = {
                "Error": "Les données contennient des caractères spéciaux. Veuillez renseigner les champs avec des données valide s'il vous plaît"
            }

            return Response(obj, status=status.HTTP_400_BAD_REQUEST)

        # On identifie l'utilisateur concerné par le changement de mot de passe
        # Puis on change son code

        queryset = Users.objects.get(user_id=request.data['user_id'])
        old_password = crypt_password(request.data['old_password'])

        if old_password == queryset.password:
            queryset.password = crypt_password(request.data['new_password'])
            queryset.save()
            return Response({"Success": "Votre mot de passe à été changé avec succès !"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"Error": "L'ancien mot de passe n'est pas correcte !"}, status=status.HTTP_401_UNAUTHORIZED)


# DetailUserView, ListUserTransactionsView, DetailUserTransactionsView, ListUserAccountsView, DetailUserAccountsView
class DetailUserView(APIView):

    def get(self, request, user_id, *args, **kargs):
        
        """ VERIFICATION DES DONNEES AVANT TRAITEMENT """

        """ TRAITEMENT DE LA REQUETE """

        queryset = get_object_or_404(Users, pk=user_id)
        serializer = DetailUserSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
# Afficher la liste des transactions pour un utilisateur d'instapay
class ListUserTransactionsView(APIView):

    def get(self, request, user_id, *args, **kargs):
        
        # Vérification des données avant traitement 
        """ VERIFICATION DES DONNEES AVANT TRAITEMENT """

        """ TRAITEMENT DE LA REQUETE """

        queryset = get_object_or_404(Users, pk=user_id)
        serializer = ListUserTransactionsSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Afficher les details d'une transactions pour un utilisateur
class DetailUserTransactionsView(APIView):
    
    def get(self, request, pk, *args, **kargs):
        pass

# Afficher la liste des comptes associé à un utilisateur
class ListUserAccountsView(APIView):

    def get(self, request, user_id, *args, **kargs):
        
        # Vérification des données avant traitement 
        """ VERIFICATION DES DONNEES AVANT TRAITEMENT """

        """ TRAITEMENT DE LA REQUETE """

        queryset = get_object_or_404(Users, pk=user_id)
        serializer = ListUserAccountsSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Afficher les détails du compte d'un utilisateur
class DetailUserAccountsView(APIView):

    def get(self, request, pk, *args, **kargs):
        pass    

class DoTransactionView(APIView):

    def post(self, request, *args, **kargs):

        # Vérification de la variable "userid" avant de l'utiliser
        checking = control_quality_data(request=request)

        if not checking:
            obj = {
                "Error": "Les données contennient des caractères spéciaux. Veuillez renseigner les champs correctement s'il vous plaît"
            }

            return Response(obj, status=status.HTTP_400_BAD_REQUEST)


        #sender = Users.objects.get(send_code=request.data['send_code'])
        sender = get_object_or_404(Users, send_code=request.data['send_code'])

        if sender.user_id == request.data['user_id']:

            #recipient = Users.objects.get(receive_code=request.data['receive_code'])
            recipient = get_object_or_404(Users, receive_code=request.data['receive_code'])
            amount = float(request.data['amount'])

            provider = Providers.objects.get(provider_name="Instapay")

            sender_account = Accounts.objects.get(owner=sender, provider=provider)
            recipient_account = Accounts.objects.get(owner=recipient, provider=provider)

            sender_funds = sender_account.amount
            if sender_funds >= amount:
                
                sender_account.amount -= amount
                recipient_account.amount += amount
                sender_account.save()
                recipient_account.save()

                # Ajouter la transaction dans la table de transaction
                transaction_id = generate_transaction_id()
                Transactions.objects.create(transaction_id=transaction_id, sender=sender, recipient=recipient, amount=amount, status="validé")
            
                # On va automatiquement changé le code d'envoie du client
                new_send_code = transfer_code_generator()
                sender.send_code = new_send_code
                sender.save()
                
                queryset = Transactions.objects.get(transaction_id=transaction_id) #>
                serializer = TransactionSerializer(queryset)

                obj = {
                    "success": "Opération reussie. Votre transaction à été éffectué avec succès !",
                    "new_send_code": new_send_code,
                    "transaction_id": serializer.data
                }
                return Response(obj, status=status.HTTP_200_OK)
            else:
                obj = {
                    "Error": "Impossible d'éffectuer la transaction. Votre compte est insuffisant"
                }
                return Response(obj, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            obj = {
                "Error": "Impossible de satisfaire votre demande !"
            }
            return Response(obj, status=status.HTTP_400_BAD_REQUEST)


class ProviderView(APIView):

    def get(self, request, *args, **kargs):

        checking = control_quality_data(request=request)

        if not checking:
            obj = {
                "Error": "Les données contennient des caractères spéciaux. Veuillez renseigner les champs correctement s'il vous plaît"
            }

            return Response(obj, status=status.HTTP_400_BAD_REQUEST)

        queryset = Providers.objects.all()
        serializer = ProviderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kargs):

        # Vérifié les données avant de les utilisés
        checking = control_quality_data(request=request)

        if not checking:
            obj = {
                "Error": "Les données contennient des caractères spéciaux. Veuillez renseigner les champs correctement s'il vous plaît"
            }

            return Response(obj, status=status.HTTP_400_BAD_REQUEST)

        request.data['provider_id'] = generate_provider_id()
        serializer = ProviderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------------------------
# JUSTE POUR LE DEVELOPPEMENT
# ------------------------------------------------

class UserView(APIView):

    def get(self, request, *args, **kargs):

        queryset = Users.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)