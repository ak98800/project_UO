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

  def modifier_button_click(self, **event_args):
    """This method is called when the component is clicked."""
    from ..ProfilEditPopup import ProfilEditPopup
    alert(ProfilEditPopup(), large=True, title="Modifier mon profil")

      


