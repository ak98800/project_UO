from ._anvil_designer import ProfilPageTemplate
from anvil import *
import anvil.users
import anvil.server

class ProfilPage(ProfilPageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user = anvil.users.get_user()

    if self.user:
      self.email_label.text = self.user["email"]

      # Récupère le profil dans la table 'profiles'
      profil = anvil.server.call("get_profil", self.user)
      if profil:
        self.name_box.text = profil["name"]
        self.organisation_box.text = profil["organisation"]
        self.fonction_box.text = profil["fonction"]
    else:
      self.email_label.text = "Non connecté"

  def save_button_click(self, **event_args):
    """Sauvegarder les modifications de profil"""
    try:
      anvil.server.call(
        "update_profil",
        self.user,
        self.name_box.text,
        self.organisation_box.text,
        self.fonction_box.text
      )
      Notification("Profil mis à jour avec succès.", style="success").show()
    except Exception as e:
      Notification(f"Erreur : {e}", style="danger").show()
