from ._anvil_designer import ParticipationItemRowTemplate
from anvil import *

class ParticipationItemRow(ParticipationItemRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    data = self.item

    self.societe_label.text = data.get("societe", "")
    self.actionnaire_label.text = data.get("actionnaire", "")
    self.pourcentage_label.text = f"{data.get('pourcentage', 0)} %"
    self.type_label.text = data.get("type", "")
    self.groupe_label.text = data.get("groupe", "")
    self.sous_groupe_label.text = data.get("sous_groupe", "")

  def delete_button_click(self, **event_args):
    if confirm(f"Supprimer la participation de {self.item['actionnaire']} dans {self.item['societe']} ?"):
      Notification("Suppression non encore implémentée", style="warning").show()



