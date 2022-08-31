from django.contrib import admin
from django.urls import path, include

#from api.views import index, UserSignin, UserLogin, UserProfile, UserTransactionView, UserView, ConfirmTransactionView, ProviderView, DoTransactionView
from api.views import index, UserSignin, UserLogin, UserProfile, UserView, ProviderView, DoTransactionView
from api.views import DetailUserView, ListUserTransactionsView, DetailUserTransactionsView, ListUserAccountsView, DetailUserAccountsView

urlpatterns = [
    path("", index, name="index"),

    # ENDPOINTS DEVELOPPEURS #
    # **************************

    # Les premières actions / Inscription, Connexion, Changement de mot de passe.
    path("signup/", UserSignin.as_view()),
    path("login/", UserLogin.as_view()),
    path("users/change_password/", UserProfile.as_view()),

    # Les utilisateurs
    path("users/<str:user_id>/", DetailUserView.as_view()), #Les informations d'un utilisateur
    path("users/<str:user_id>/transactions/", ListUserTransactionsView.as_view()), #Afficher la liste des transactions pour un utilisateur
    path("users/<str:user_id>/transactions/?provider=<str:provider_name>", DetailUserTransactionsView.as_view()), #Transactions impliquant un provider spécifique
    path("users/<str:user_id>/accounts/", ListUserAccountsView.as_view()), #Tous les comptes 
    path("users/<str:user_id>/accounts/?provider=<str:provider_name>/", DetailUserAccountsView.as_view()), #Les comptes d'un provider spécifique

    # Les Transactions
    path("transactions/", DoTransactionView.as_view()), #Faire une transactions

    # Les providers
    path("providers/", ProviderView.as_view()), #Afficher les providers

    # Juste pour le dévéloppement
    path("users/", UserView.as_view()), #Afficher touts les utilisateurs
]
