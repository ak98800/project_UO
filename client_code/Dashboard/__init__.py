from ._anvil_designer import DashboardTemplate
from anvil import *
import anvil.users

class Dashboard(DashboardTemplate):
  def __init__(self, user=None, **properties):
    self.init_components(**properties)
    self.user = user or anvil.users.get_user()

    if self.user:
      self.label_welcome.text = f"Bienvenue, {self.user['email']} !"
    else:
      self.label_welcome.text = "Bienvenue !"



