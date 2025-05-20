from ._anvil_designer import mainpageTemplate
from anvil import *
import anvil.server
import anvil.users

class mainpage(mainpageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Évite toute redirection si un utilisateur est déjà connecté
    user = anvil.users.get_user()
    if user:
      # Ne rien faire, car LoginPage → HomePageLayout a déjà été chargé
      return

    # Sinon, affichage LandingPage avec boutons
    self.se_connecter.visible = True
    self.inscription.visible = True

    from ..LandingPage import LandingPage
    self.content_panel.clear()
    self.content_panel.add_component(LandingPage())

  def se_connecter_click(self, **event_args):
    from ..LoginPage import LoginPage
    open_form(LoginPage())

  def inscription_click(self, **event_args):
    from ..SignUpPage import SignUpPage
    open_form(SignUpPage())
