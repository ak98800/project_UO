from ._anvil_designer import SignUpPageTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables

class SignUpPage(SignUpPageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def signup_button_click(self, **event_args):
    name = self.name_textbox.text
    organisation = self.organisation_textbox.text
    fonction = self.fonction_textbox.text
    email = self.email_textbox.text
    password = self.password_textbox.text
    confirm_password = self.confirm_password_textbox.text

    if not (name and organisation and fonction and email and password and confirm_password):
      Notification("Merci de remplir tous les champs obligatoires.", style="warning").show()
      return

    if password != confirm_password:
      Notification("Les mots de passe ne correspondent pas.", style="danger").show()
      return

    try:
      user = anvil.users.signup_with_email(email, password)

      if user:
        # 1. Enregistrer les infos dans la table 'profiles' via le serveur
        anvil.server.call("enregistrer_profil", user, name, organisation, fonction)



        Notification(
          "Votre compte a été créé. Un email de confirmation a été envoyé. Veuillez le valider avant de vous connecter.",
          style="info"
        ).show()

                # 3. Déconnecter l’utilisateur immédiatement (il ne peut rien faire avant confirmation)
        anvil.users.logout()

        # Redirection simple vers la page de connexion
        from ..LoginPage import LoginPage
        get_open_form().load_page(LoginPage())

    except Exception as e:
      Notification(f"Erreur lors de la création du compte : {e}", style="danger").show()
