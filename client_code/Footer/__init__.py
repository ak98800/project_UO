from ._anvil_designer import FooterTemplate
from anvil import *

class Footer(FooterTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.footer_label.text = "© 2025 UltimateOwner — Tous droits réservés"
    self.footer_label.align = "center"
    self.footer_label.role = "footer"

