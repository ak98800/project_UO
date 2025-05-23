from ._anvil_designer import MesDossiersTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.users

from ..NavigationBar import NavigationBar
from DossierItemRow import DossierItemRow

class MesDossiers(MesDossiersTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.repeating_dossiers.set_event_handler("x-reload-dossiers", self.repeating_dossiers_x_reload_dossiers)


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

  def recharger_profil(self):
    try:
      self.profil = anvil.server.call("get_profil", self.user)

      if self.profil:
        self.recharger_dossiers()
      else:
        Notification("Profil introuvable.", style="danger").show()
    except Exception as e:
      Notification(f"Erreur de profil : {e}", style="danger").show()

  def recharger_dossiers(self):
    try:
      dossiers = anvil.server.call("get_dossiers", self.profil["organisation"])
      self.repeating_dossiers.items = dossiers
    except Exception as e:
      Notification(f"Erreur lors du chargement des dossiers : {e}", style="danger").show()

  def creer_dossier_button_click(self, **event_args):
    nom_dossier = self.nom_dossier_textbox.text.strip()
    if not nom_dossier:
      Notification("Veuillez entrer un nom de dossier.", style="warning").show()
      return

    try:
      anvil.server.call("creer_dossier", nom_dossier, self.profil)
      Notification("Dossier créé avec succès !", style="success").show()
      self.nom_dossier_textbox.text = ""
      self.recharger_dossiers()
    except Exception as e:
      Notification(f"Erreur : {e}", style="danger").show()

  def repeating_dossiers_show(self, **event_args):
    pass


  def repeating_dossiers_x_reload_dossiers(self, **event_args):
    self.recharger_dossiers()



