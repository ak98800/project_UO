from ._anvil_designer import HomePageLayoutTemplate
from anvil import *
import anvil.users

# Import direct des pages à afficher
from Dashboard import Dashboard
from ProfilPage import ProfilPage
from GestionUtilisateursPage import GestionUtilisateursPage

class HomePageLayout(HomePageLayoutTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user = anvil.users.get_user()

    print("✅ HomePageLayout actif")

    # 🔍 Debug : voir si le slot est bien reconnu
    print("🔍 Composants dans HomePageLayout :")
    for name in dir(self):
      if not name.startswith("_"):
        attr = getattr(self, name)
        if isinstance(attr, Component):
          print(f"- {name} ({type(attr)})")

    # Affiche le Dashboard au démarrage
    self.afficher_page(Dashboard(user=self.user))

  def afficher_page(self, page):
    # Affiche dynamiquement la page dans le slot prévu
    try:
      self.slot_content.clear()
      self.slot_content.add_component(page)
    except AttributeError:
      Notification("⚠️ Le slot 'slot_content' est introuvable. Vérifie qu'il est bien ajouté dans le Designer.", style="danger").show()
      print("❌ ERREUR : 'slot_content' non trouvé dans le layout.")

  def navigation_link_dashboard_click(self, **event_args):
    self.afficher_page(Dashboard(user=self.user))

  def navigation_link_profil_click(self, **event_args):
    self.afficher_page(ProfilPage())

  def navigation_link_utilisateurs_click(self, **event_args):
    self.afficher_page(GestionUtilisateursPage())

  def navigation_link_logout_click(self, **event_args):
    anvil.users.logout()
    open_form("mainpage")
