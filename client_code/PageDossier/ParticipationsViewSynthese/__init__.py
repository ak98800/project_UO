from ._anvil_designer import ParticipationsViewSyntheseTemplate
from anvil import *
import anvil.server

class ParticipationsViewSynthese(ParticipationsViewSyntheseTemplate):
  def __init__(self, dossier, **properties):
    self.init_components(**properties)
    self.dossier = dossier

    # Chargement des données avec injection du dossier dans chaque ligne
    societes = anvil.server.call("get_synthese_participations", self.dossier["id"])
    for s in societes:
      s["dossier"] = self.dossier
    self.repeating_panel.items = societes

  def ajouter_societe_button_click(self, **event_args):
    from .PopupAjouterSociete import PopupAjouterSociete
    popup = PopupAjouterSociete(dossier=self.dossier)
    popup.set_event_handler("x-societe-prete", self._ouvrir_fiche_nouvelle_societe)
    alert(popup, large=True, buttons=[])

  def _ouvrir_fiche_nouvelle_societe(self, nom_societe=None, **event_args):
    # 💾 Appelle le serveur pour initialiser la société
    anvil.server.call("initialiser_societe", self.dossier["id"], nom_societe)

    # 👉 Ouvre la fiche société en tant que page dédiée (et non plus dans zone_contenu)
    from ..PageFicheParticipation import PageFicheParticipation
    open_form(PageFicheParticipation(dossier=self.dossier, nom_societe=nom_societe))















