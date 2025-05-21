from ._anvil_designer import DashboardTemplate
from anvil import *
import anvil.users

from ..NavigationBar import NavigationBar  # Assure-toi que ce fichier existe

class Dashboard(DashboardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # ✅ Appliquer le rôle sticky au header
    self.header_panel.role = "sticky-header"

    # ✅ Appliquer le rôle scrollable au contenu
    self.content_panel.role = "scrollable-content"

    # ✅ Ajouter la barre de navigation à gauche
    self.navigation_bar_panel.clear()
    self.navigation_bar_panel.add_component(NavigationBar())

    # ✅ Message de bienvenue
    user = anvil.users.get_user()
    self.label_welcome.text = f"Bienvenue, {user['email']}" if user else "Bienvenue !"



