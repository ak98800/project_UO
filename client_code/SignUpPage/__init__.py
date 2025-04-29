from ._anvil_designer import SignUpPageTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
from anvil.tables import app_tables

class SignUpPage(SignUpPageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def signup_button_click(self, **event_args):
    """Quand on clique sur 'Créer mon compte'"""
    name = self.name_textbox.text
    organisation = self.organisation_textbox.text
    fonction = self.fonction_textbox.text
    email = self.email_textbox.text
    password = self.password_textbox.text
    confirm_password = self.confirm_password_textbox.text

    # Vérifier que tous les champs sont remplis
    if not (name and organisation and fonction and email and password and confirm_password):
      Notification("Merci de remplir tous les champs obligatoires.", style="warning").show()
      return

    # Vérifier que les mots de passe correspondent
    if password != confirm_password:
      Notification("Les mots de passe ne correspondent pas.", style="danger").show()
      return

    # Créer l'utilisateur
    try:
      user = anvil.users.signup_with_email(email, password)

      if user:
        # Stocker les autres informations
        app_tables.users.update_or_insert(
          user=user,
          name=name,
          organisation=organisation,
          fonction=fonction
        )

        Notification("Compte créé avec succès !", style="success").show()
        from ..Dashboard import Dashboard
        get_open_form().load_page(Dashboard())

    except anvil.users.SignupError:
      Notification("Impossible de créer le compte. Essayez un autre email.", style="danger").show()



