from ._anvil_designer import ParticipationItemRowTemplate
from anvil import *
import anvil.server

class ParticipationItemRow(ParticipationItemRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.actionnaire_label.text = self.item.get("actionnaire", "")
    self.type_label.text = self.item.get("type_actionnaire", "")

    pct = self.item.get("pourcentage", None)
    self.pourcentage_label.text = f"{round(pct, 2)} %" if pct is not None else "-"

    parts = self.item.get("nb_parts", None)
    self.nb_parts_label.text = str(int(parts)) if parts is not None else "-"

  def delete_link_click(self, **event_args):
    if confirm(f"Supprimer {self.item['actionnaire']} ?"):
      anvil.server.call("supprimer_participation", self.item["id"])
      Notification("Supprimé", style="success").show()
      self.parent.parent.refresh_fiche_participation()






