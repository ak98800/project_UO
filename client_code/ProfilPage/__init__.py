from ._anvil_designer import ProfilPageTemplate
from anvil import *
import anvil.users
import anvil.server

class ProfilPage(ProfilPageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user = anvil.users.get_user()

    self.profil = None

    if self.user:
      self.email_label.text = self.user["email"]

      self.profil = anvil.server.call("get_profil", self.user)

      if self.profil:
        self.name_box.text = self.profil["name"]
        self.fonction_box.text = self.profil["fonction"]

        # Organisation (modifiable uniquement si admin)
        if self.profil["organisation"]:
          self.organisation_box.text = self.profil["organisation"]["name"]
          if self.profil["is_admin"]:
            self.organisation_box.enabled = True
          else:
            self.organisation_box.enabled = False
        else:
          self.organisation_box.text = "Aucune"
          self.organisation_box.enabled = False
      else:
        Notification("Profil introuvable.", style="danger").show()
    else:
      Notification("Utilisateur non connecté.", style="danger").show()

  def save_button_click(self, **event_args):
    """Enregistrer les modifications de nom, fonction et organisation si admin"""
    try:
      # Nom et fonction
      anvil.server.call("update_profil", self.user, self.name_box.text, self.fonction_box.text)

      # Organisation si admin
      if self.profil and self.profil["is_admin"]:
        anvil.server.call("update_organisation_name", self.profil["organisation"], self.organisation_box.text)

      Notification("Profil mis à jour avec succès.", style="success").show()
    except Exception as e:
      Notification(f"Erreur : {e}", style="danger").show()
