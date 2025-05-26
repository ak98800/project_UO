from ._anvil_designer import PopupAjouterActionnaireTemplate
from anvil import *
import anvil.server

class PopupAjouterActionnaire(PopupAjouterActionnaireTemplate):
  def __init__(self, dossier, nom_societe, **properties):
    self.init_components(**properties)
    self.dossier = dossier
    self.societe = nom_societe

  def ajouter_button_click(self, **event_args):
    nom = self.nom_textbox.text.strip()
    type_act = self.type_dropdown.selected_value
    nb_parts = self.nb_parts_textbox.text.strip()
    pourcentage = self.pourcentage_textbox.text.strip()
    calcul_auto = self.calcul_auto_checkbox.checked

    if not nom:
      Notification("Nom de l'actionnaire requis.", style="warning").show()
      return

    try:
      res = anvil.server.call(
        "ajouter_participation_actionnaire",
        self.dossier["id"],
        self.societe,
        nom,
        type_act,
        nb_parts,
        pourcentage,
        calcul_auto
      )
      Notification("Actionnaire ajouté avec succès.", style="success").show()
      self.raise_event("x-actionnaire-ajoute")
      self.raise_event("x-close-alert")
    except Exception as e:
      Notification(str(e), style="danger").show()

  def annuler_button_click(self, **event_args):
    """This method is called when the component is clicked."""
    self.raise_event("x-close-alert")







