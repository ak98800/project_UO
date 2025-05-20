from ._anvil_designer import HomePageLayoutTemplate
from anvil import *
import anvil.users
from ..Dashboard import Dashboard
from ..ProfilPage import ProfilPage
from ..GestionUtilisateursPage import GestionUtilisateursPage

class HomePageLayout(HomePageLayoutTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user = anvil.users.get_user()

    print("✅ HomePageLayout actif")

    self.footer_label.role = "footer"
    self.afficher_dashboard()

  def afficher_dashboard(self):
    print("🔁 Dashboard affiché")
    self.content_panel.clear()
    self.content_panel.add_component(Dashboard(user=self.user))

  def afficher_profil(self):
    print("🔁 ProfilPage affichée")
    self.content_panel.clear()
    self.content_panel.add_component(ProfilPage())

  def afficher_utilisateurs(self):
    print("🔁 GestionUtilisateursPage affichée")
    self.content_panel.clear()
    self.content_panel.add_component(GestionUtilisateursPage())

  def navigation_link_dashboard_click(self, **event_args):
    self.afficher_dashboard()

  def navigation_link_profil_click(self, **event_args):
    self.afficher_profil()

  def navigation_link_utilisateurs_click(self, **event_args):
    self.afficher_utilisateurs()

  def navigation_link_logout_click(self, **event_args):
    anvil.users.logout()
    open_form("mainpage")  # <- retour à la page d’accueil (pré-login)
