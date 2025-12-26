from ._anvil_designer import AnalyseSocietePageTemplate
from anvil import *
import anvil.server
import anvil.users

from ..VueDescendateView import VueDescendateView
from ..VueMontanteView import VueMontanteView
from ..BeneficiairesEffectifsView import BeneficiairesEffectifsView
from ..RapportSocietePage import RapportSocietePage



class AnalyseSocietePage(AnalyseSocietePageTemplate):
  def __init__(self, dossier=None, **properties):
    self.init_components(**properties)

    self.dossier = dossier

    # Charger les sociétés du dossier
    self.societes = anvil.server.call('get_liste_societes_du_dossier', self.dossier['name'])

    # items = (label affiché, value)
    self.dropdown_societe.items = [(s["name"], s) for s in self.societes]

    # Précharger la première société automatiquement
    if self.societes:
      self.dropdown_societe.selected_value = self.societes[0]
      self._charger_vue_descendante()

  def _get_societe_nom_ui(self):
    """Retourne le NOM de société réellement sélectionné/tapé dans l'UI."""
    value = self.dropdown_societe.selected_value

    # Cas 1 : la value est le dict société
    if isinstance(value, dict):
      return value.get("name")

    # Cas 2 : la value est une string (si ton composant le permet)
    if isinstance(value, str):
      return value.strip()

    # Cas 3 : rien / autre
    return None

  def dropdown_societe_change(self, **event_args):
    societe_nom = self._get_societe_nom_ui()
    print(f"🔁 Société sélectionnée (UI) : {societe_nom} | raw={self.dropdown_societe.selected_value}")
    self._charger_vue_descendante()

  def _charger_vue_descendante(self, **event_args):
    societe_nom = self._get_societe_nom_ui()

    if not societe_nom:
      alert("Aucune société sélectionnée.")
      return

    print(f"🔄 Chargement de VueDescendateView pour : {societe_nom}")

    self.content_panel.clear()
    self.content_panel.add_component(
      VueDescendateView(
        dossier=self.dossier,
        societe_point_depart=societe_nom
      )
    )

  def _charger_vue_montante(self, **event_args):
    societe_nom = self._get_societe_nom_ui()
    if not societe_nom:
      alert("Aucune société sélectionnée.")
      return

    self.content_panel.clear()
    self.content_panel.add_component(
      VueMontanteView(
        dossier=self.dossier,
        societe_point_depart=societe_nom
      )
    )

  def _charger_vue_beneficiaires(self, **event_args):
    societe_nom = self._get_societe_nom_ui()
    if not societe_nom:
      alert("Aucune société sélectionnée.")
      return

    self.content_panel.clear()
    self.content_panel.add_component(
      BeneficiairesEffectifsView(
        dossier=self.dossier,
        societe_point_depart=societe_nom
      )
    )

  def _charger_vue_rapport(self, **event_args):
    value = self.dropdown_societe.selected_value
    societe_obj = value if isinstance(value, dict) else None
    if not societe_obj:
      alert("Veuillez sélectionner une société (liste) pour le rapport.")
      return

    self.content_panel.clear()
    self.content_panel.add_component(
      RapportView(societe=societe_obj)
    )

  def btn_vue_descendante_click(self, **event_args):
    self._charger_vue_descendante()

  def btn_vue_montante_click(self, **event_args):
    self._charger_vue_montante()

  @handle("btn_beneficiaires", "click")
  def btn_beneficiaires_click(self, **event_args):
    self._charger_vue_beneficiaires()


  def _charger_vue_rapport(self, **event_args):
    societe_nom = self._get_societe_nom_ui()
    if not societe_nom:
      alert("Aucune société sélectionnée.")
      return

    self.content_panel.clear()
    self.content_panel.add_component(
      RapportSocietePage(
        dossier=self.dossier,
        societe=societe_nom
      )
    )
    
  @handle("btn_rapport", "click")
  def btn_rapport_click(self, **event_args):
    self._charger_vue_rapport()








