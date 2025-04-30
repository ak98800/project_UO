from ._anvil_designer import HomepageLayoutTemplate
from anvil import *
import anvil.users
import anvil.server
from ..StripePricing import StripePricing
from ..Dashboard import Dashboard

class HomepageLayout(HomepageLayoutTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.check_upgrade_nav_link()
    self.load_page(Dashboard())  # Par défaut, on affiche le Dashboard

  def check_upgrade_nav_link(self):
    user = anvil.users.get_user()
    if user:
      if user["subscription"] == "Free" or not user["subscription"]:
        self.upgrade_navigation_link.visible = True
      else:
        self.upgrade_navigation_link.visible = False
    else:
      self.upgrade_navigation_link.visible = False

  def load_page(self, page_instance):
    self.content_panel.clear()
    self.content_panel.add_component(page_instance)

  def logout_navigation_link_click(self, **event_args):
    anvil.users.logout()
    Notification("Déconnecté avec succès.", style="info").show()
    from ..mainpage import mainpage
    open_form(mainpage())

  def stripe_pricing_link_click(self, **event_args):
    alert(StripePricing(), large=True)
    self.check_upgrade_nav_link()

  def navigation_link_1_click(self, **event_args):
    self.load_page(Dashboard())
