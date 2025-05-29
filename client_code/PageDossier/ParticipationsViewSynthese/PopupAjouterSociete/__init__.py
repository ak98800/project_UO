from ._anvil_designer import PopupAjouterSocieteTemplate
from anvil import *
import anvil.server

class PopupAjouterSociete(PopupAjouterSocieteTemplate):
  def __init__(self, dossier, **properties):
    self.init_components(**properties)
    self.dossier = dossier

  def ajouter_button_click(self, **event_args):
    nom = self.nom_textbox.text.strip()

    if not nom:
      Notification("Veuillez entrer un nom de société.", style="warning").show()
      return

    try:
      # Vérifie l’unicité et retourne le nom si OK
      nom_valide = anvil.server.call("verifier_societe_unique", self.dossier["id"], nom)
      self.raise_event("x-societe-prete", nom_societe=nom_valide)
      self.raise_event("x-close-alert")
    except Exception as e:
      Notification(str(e), style="danger").show()

  def annuler_button_click(self, **event_args):
    self.raise_event("x-close-alert")



