from ._anvil_designer import HomepageLayoutTemplate
from anvil import *
import anvil.users
import anvil.server

class HomepageLayout(HomepageLayoutTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Optionnel : Affiche la page d'accueil ou un dashboard par défaut
    from ..Dashboard import Dashboard
    self.content_slot.clear()
    self.content_slot.add_component(Dashboard())

  def load_page(self, page):
    """Méthode appelée pour charger dynamiquement une page dans le slot"""
    self.content_slot.clear()
    self.content_slot.add_component(page)
