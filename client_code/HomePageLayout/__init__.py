from ._anvil_designer import HomePageLayoutTemplate
from anvil import *
import anvil.users
from ..Dashboard import Dashboard

class HomePageLayout(HomePageLayoutTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user = anvil.users.get_user()

    # Charger Dashboard par défaut
    self.content_panel.clear()
    self.content_panel.add_component(Dashboard(user=self.user))
