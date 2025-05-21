from ._anvil_designer import DashboardTemplate
from anvil import *
import anvil.users
from ..NavigationBar import NavigationBar

class Dashboard(DashboardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Header : affiche le message
    user = anvil.users.get_user()
    self.label_welcome.text = f"Bienvenue, {user['email']}" if user else "Bienvenue !"

    # NavigationBar à gauche
    self.navigation_panel.add_component(NavigationBar())

    # Footer si besoin
    self.footer_label.text = "© 2025 Ultimate"
