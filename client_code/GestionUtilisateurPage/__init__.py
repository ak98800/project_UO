from ._anvil_designer import GestionUtilisateurPageTemplate
from anvil import *
import anvil.server
import anvil.users

from ..NavigationBar import NavigationBar

class GestionUtilisateurPage(GestionUtilisateurPageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Mise en page
    self.header_panel.role = "sticky-header"
    self.content_panel.role = "scrollable-content"
    self.navigation_bar_panel.clear()
    self.navigation_bar_panel.add_component(NavigationBar())

    # Authentification
    self.user = anvil.users.get_user()
    self.profil = None

    if self.user:
      self.label_welcome.text = f"Bienvenue, {self.user['email']}"
      self.recharger_profil()
    else:
      Notification("Utilisateur non connecté.", style="danger").show()
      self.label_welcome.text = "Bienvenue !"

    # Écoute de l’événement de rafraîchissement depuis UserItemRow
    self.users_panel.set_event_handler("x-refresh", self.recharger_utilisateurs)

  def recharger_profil(self):
    self.profil = anvil.server.call("get_profil", self.user)

    if self.profil:
      if not self.profil["is_admin"]:
        Notification("Accès réservé aux administrateurs.", style="danger").show()
        return

      self.recharger_utilisateurs()
    else:
      Notification("Profil introuvable.", style="danger").show()

  def recharger_utilisateurs(self):
    try:
      users = anvil.server.call("lister_utilisateurs_organisation", self.profil["organisation"])
      self.users_panel.items = users
    except Exception as e:
      Notification(f"Erreur lors du chargement des utilisateurs : {e}", style="danger").show()

  def inviter_button_click(self, **event_args):
    email = self.email_textbox.text.strip()
    name = self.name_textbox.text.strip()
  
    if not email or not name:
      Notification("Veuillez entrer un nom et un email.", style="warning").show()
      return
  
    try:
      msg = anvil.server.call("inviter_utilisateur", email, name, self.profil["organisation"])
      Notification(msg, style="success").show()
      self.email_textbox.text = ""
      self.name_textbox.text = ""
      self.recharger_utilisateurs()
    except Exception as e:
      Notification(f"Erreur : {e}", style="danger").show()


  def users_panel_x_refresh(self, **event_args):
    self.recharger_utilisateurs()

