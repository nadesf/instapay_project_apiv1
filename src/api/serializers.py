from rest_framework.serializers import ModelSerializer

from api.models import Users, Providers, Transactions, Accounts



class UserSigninSerializer(ModelSerializer):
    
    class Meta:
        model = Users
        fields = ["user_id", "first_name", "last_name", "contact", "send_code", "receive_code", "status_user", "name_pointofsale", "location"]

class AccountSerializer(ModelSerializer):

    class Meta:
        model = Accounts
        fields = ["owner", "amount", "status_account", "provider"]

class TransactionSerializer(ModelSerializer):

    class Meta:
        model = Transactions
        fields = ["sender", "recipient", "amount", "datetime", "status"]

# DetailUserSerializer, ListUserTransactionsVSerializer, ListUserAccountsSerializer

class DetailUserSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = ["user_id", "first_name", "last_name", "contact", "send_code", "receive_code"]

class ListUserAccountsSerializer(ModelSerializer):

    account_owner = AccountSerializer(many=True)

    class Meta:
        model = Users 
        fields = ["user_id", "first_name", "last_name", "contact", "send_code", "receive_code", "account_owner"]


class ListUserTransactionsSerializer(ModelSerializer):

    user_sender = TransactionSerializer(many=True)

    class Meta:
        model = Users
        fields = ["user_id", "first_name", "last_name", "contact", "send_code", "receive_code", "user_sender"]

class ProviderSerializer(ModelSerializer):

    class Meta:
        model = Providers
        fields = ["provider_id", "provider_name", "active"]

# --------------------------------------
# JUSTE POUR LE DEVELOPPEMENT
# --------------------------------------

class UserSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = ["user_id", "first_name", "last_name", "contact", "password", "active", "status_user", "date_created"]