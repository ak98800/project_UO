from ._anvil_designer import DashboardTemplate
from anvil import *
import anvil.server
import anvil.users
# Assure-toi d’importer tes autres pages :
# from ..DossiersPage import DossiersPage
# from ..FichiersPage import FichiersPage
# etc.

class Dashboard(DashboardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user = anvil.users.get_user()


    # Message de bienvenue
    if self.user:
      email = self.user["email"]
      self.label_welcome.text = f"Bienvenue, {email} !"
    else:
      self.label_welcome.text = "Bienvenue !"


