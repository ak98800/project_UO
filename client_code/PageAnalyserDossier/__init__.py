from ._anvil_designer import PageAnalyserDossierTemplate
from anvil import *
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.users

from ..NavigationBar import NavigationBar
from ..OrganigrammeView import OrganigrammeView

class PageAnalyserDossier(PageAnalyserDossierTemplate):
  def __init__(self, dossier=None, **properties):
    self.init_components(**properties)

    self.user = anvil.users.get_user()
    self.profil = anvil.server.call("get_profil", self.user)

    # ✅ UI setup
    self.header_panel.role = "sticky-header"
    self.content_panel.role = "scrollable-content"
    self.navigation_bar_panel.clear()
    self.navigation_bar_panel.add_component(NavigationBar())

    self.label_welcome.text = f"Bienvenue, {self.user['email']}" if self.user else "Bienvenue !"

    # ✅ Charger les dossiers
    self.dossiers = anvil.server.call("get_dossiers", self.profil["organisation"])
    self.dropdown_dossiers.items = [(d["name"], d) for d in self.dossiers]

    # ✅ Pré-sélection si dossier passé en paramètre
    if dossier:
      self.dossier = dossier
      self.dropdown_dossiers.selected_value = dossier
      self._afficher_organigramme()
    else:
      self.dossier = None
      self.zone_contenu.clear()
      self.zone_contenu.add_component(Label(text="Veuillez sélectionner un dossier pour commencer l’analyse.", italic=True))

  def dropdown_dossiers_change(self, **event_args):
    # ⚡ Mise à jour immédiate dès la sélection
    self.dossier = self.dropdown_dossiers.selected_value
    if self.dossier:
      self._afficher_organigramme()

  def analyser_button_click(self, **event_args):
    # 🛡️ Double sécurité au cas où
    self.dossier = self.dropdown_dossiers.selected_value
    if self.dossier:
      self._afficher_organigramme()
    else:
      alert("Veuillez sélectionner un dossier avant d’analyser.")

  def _afficher_organigramme(self):
    self.zone_contenu.clear()
    self.zone_contenu.add_component(OrganigrammeView(dossier=self.dossier))

  def btn_analyse_societe_click(self, **event_args):
    if self.dossier:
      from ..AnalyseSocietePage import AnalyseSocietePage
      self.zone_contenu.clear()
      self.zone_contenu.add_component(AnalyseSocietePage(dossier=self.dossier))

