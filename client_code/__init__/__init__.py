from ._anvil_designer import __init__Template
from anvil import *
import anvil.users

class __init__(__init__Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    user = anvil.users.get_user()

    if user and user["enabled"]:
        # Utilisateur connecté avec email confirmé
        from .mainpage import mainpage
        open_form(mainpage())
    else:
        # Par défaut : rediriger vers mainpage avec confirmed=True
        from .mainpage import mainpage
        open_form(mainpage(confirmed=True))

