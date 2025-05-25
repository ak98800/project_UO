from ._anvil_designer import ParticipationsViewSyntheseTemplate
from anvil import *
import anvil.server

class ParticipationsViewSynthese(ParticipationsViewSyntheseTemplate):
  def __init__(self, dossier, **properties):
    self.init_components(**properties)
    self.dossier = dossier

    # Chargement des données synthétiques du dossier
    self.repeating_panel.items = anvil.server.call("get_synthese_participations", self.dossier["id"])
    # Dans __init__
    self.repeating_panel.set_event_handler("x-ouvrir-fiche", self._rediriger_vers_fiche)


  def ajouter_societe_button_click(self, **event_args):
    from ..PopupAjouterSociete import PopupAjouterSociete
    popup = PopupAjouterSociete(self.dossier)
    popup.set_event_handler("x-societe-prete", self._rediriger_vers_fiche)
    alert(popup, large=True, buttons=[])

  def _rediriger_vers_fiche(self, nom_societe=None, **event_args):
    if nom_societe:
      from ..PageFicheParticipation import PageFicheParticipation
      fiche = PageFicheParticipation(dossier=self.dossier, nom_societe=nom_societe)
      self.parent.raise_event("x-afficher-fiche-societe", composant=fiche)







