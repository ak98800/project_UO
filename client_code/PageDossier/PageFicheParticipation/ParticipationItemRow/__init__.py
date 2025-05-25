from ._anvil_designer import ParticipationItemRowTemplate
from anvil import *

class ParticipationItemRow(ParticipationItemRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    data = self.item

    self.actionnaire_label.text = data.get("actionnaire", "")
    self.type_label.text = data.get("type_actionnaire", "")

    pct = data.get("pourcentage", None)
    self.pourcentage_label.text = f"{round(pct, 2)} %" if pct is not None else "-"

    parts = data.get("nb_parts", None)
    self.nb_parts_label.text = str(int(parts)) if parts is not None else "-"


  def delete_link_click(self, **event_args):
    if confirm(f"Supprimer {self.item['actionnaire']} ?"):
      # À implémenter : suppression réelle côté serveur
      Notification("Suppression à venir.", style="warning").show()

