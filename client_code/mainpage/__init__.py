from ._anvil_designer import mainpageTemplate
from anvil import *
import anvil.server
import anvil.users

class mainpage(mainpageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Vérifie s'il y a un utilisateur connecté
    user = anvil.users.get_user()

    if user:
      try:
        # Récupère le profil utilisateur
        profil = anvil.server.call("get_profil", user)

        # ✅ Si invité confirmé (non-admin)
        if profil and not profil["is_admin"] and user.get("email_confirmed", False):
          from ..WelcomeResetPage import WelcomeResetPage
          open_form(WelcomeResetPage())
          return

        # ✅ Sinon, utilisateur standard → Dashboard
        from ..Dashboard import Dashboard
        open_form(Dashboard())
        return

      except Exception as e:
        Notification(f"Erreur lors du chargement du profil : {e}", style="danger").show()
        self.charger_landing()
        return

    # Aucun utilisateur connecté → LandingPage
    self.charger_landing()

  def charger_landing(self):
    self.se_connecter.visible = True
    self.inscription.visible = True

    from ..LandingPage import LandingPage
    self.content_panel.clear()
    self.content_panel.add_component(LandingPage())

  def se_connecter_click(self, **event_args):
    from ..LoginPage import LoginPage
    self.content_panel.clear()
    self.content_panel.add_component(LoginPage())
    
  def inscription_click(self, **event_args):
    from ..SignUpPage import SignUpPage
    self.content_panel.clear()
    self.content_panel.add_component(SignUpPage())