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
      self.recharger_profil()
    else:
      Notification("Utilisateur non connecté.", style="danger").show()

  def recharger_profil(self):
    self.profil = anvil.server.call("get_profil", self.user)

    if self.profil:
      self.name_box.text = self.profil["name"]
      self.fonction_box.text = self.profil["fonction"]

      if self.profil["organisation"]:
        self.organisation_box.text = self.profil["organisation"]["name"]
        self.organisation_box.enabled = self.profil["is_admin"]
      else:
        self.organisation_box.text = "Aucune"
        self.organisation_box.enabled = False
    else:
      Notification("Profil introuvable.", style="danger").show()

  def modifier_button_click(self, **event_args):
    from ..ProfilEditPopup import ProfilEditPopup
    result = alert(ProfilEditPopup(), title="Modifier mon profil", large=True, buttons=None)
    if result is True:
      self.recharger_profil()



      


