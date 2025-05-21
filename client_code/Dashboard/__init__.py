from ._anvil_designer import DashboardTemplate
from anvil import *
from ..NavigationBar import NavigationBar
import anvil.users

class Dashboard(DashboardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # ✅ Affiche la barre de navigation
    self.navigation_bar_panel.add_component(NavigationBar())

    # Message de bienvenue
    user = anvil.users.get_user()
    self.label_welcome.text = f"Bienvenue, {user['email']}" if user else "Bienvenue !"








