from ._anvil_designer import AnalyseSocietePage_copyTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.users

from ..VueDescendateView import VueDescendateView
from ..VueMontanteView import VueMontanteView
from ..BeneficiairesEffectifsView import BeneficiairesEffectifsView
from ..RapportView import RapportView


class AnalyseSocietePage_copy(AnalyseSocietePage_copyTemplate):
  def __init__(self, dossier=None, **properties):
    self.init_components(**properties)

    self.dossier = dossier
    self.societe_selectionnee = None

    # Charger les sociétés du dossier
    self.societes = anvil.server.call(
      "get_liste_societes_du_dossier", self.dossier["name"]
    )
    self.dropdown_societe.items = [(s["name"], s) for s in self.societes]

    # Précharger la première société automatiquement
    if self.societes:
      self.societe_selectionnee = self.societes[0]
      self.dropdown_societe.selected_value = self.societe_selectionnee
      self._charger_vue_descendante()

  def dropdown_societe_change(self, **event_args):
    self.societe_selectionnee = self.dropdown_societe.selected_value
    print(f"🔁 Société sélectionnée : {self.societe_selectionnee['name']}")
    self._charger_vue_descendante()

  def _charger_vue_descendante(self, **event_args):
    if self.societe_selectionnee:
      societe_nom = self.societe_selectionnee["name"]
      print(f"🔄 Chargement de VueDescendateView pour : {societe_nom}")
      self.content_panel.clear()
      self.content_panel.add_component(
        VueDescendateView(dossier=self.dossier, societe_point_depart=societe_nom)
      )

  def _charger_vue_montante(self, **event_args):
    if self.societe_selectionnee:
      self.content_panel.clear()
      self.content_panel.add_component(
        VueMontanteView(societe=self.societe_selectionnee)
      )

  def _charger_vue_beneficiaires(self, **event_args):
    if self.societe_selectionnee:
      self.content_panel.clear()
      self.content_panel.add_component(
        BeneficiairesEffectifsView(societe=self.societe_selectionnee)
      )

  def _charger_vue_rapport(self, **event_args):
    if self.societe_selectionnee:
      self.content_panel.clear()
      self.content_panel.add_component(RapportView(societe=self.societe_selectionnee))

  def btn_vue_descendante_click(self, **event_args):
    self._charger_vue_descendante()

  def btn_vue_montante_click(self, **event_args):
    self._charger_vue_montante()

  def btn_beneficiaires_click(self, **event_args):
    self._charger_vue_beneficiaires()

  def btn_rapport_click(self, **event_args):
    self._charger_vue_rapport()
