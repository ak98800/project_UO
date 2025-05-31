from ._anvil_designer import NavigationBarTemplate
from anvil import *
import anvil.users

class NavigationBar(NavigationBarTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def navigation_link_dashboard_click(self, **event_args):
    from Dashboard import Dashboard
    open_form(Dashboard())

  def navigation_link_profil_click(self, **event_args):
    from ProfilPage import ProfilPage
    open_form(ProfilPage())

  def navigation_link_utilisateurs_click(self, **event_args):
    from GestionUtilisateurPage import GestionUtilisateurPage
    open_form(GestionUtilisateurPage())

  def navigation_link_logout_click(self, **event_args):
    anvil.users.logout()
    open_form("mainpage")


  def navigation_link_dossiers_click(self, **event_args):
    from MesDossiers import MesDossiers
    open_form(MesDossiers())

  def navigation_link_analyse_click(self, **event_args):
    from PageAnalyserDossier import PageAnalyserDossier
    open_form(PageAnalyserDossier())

