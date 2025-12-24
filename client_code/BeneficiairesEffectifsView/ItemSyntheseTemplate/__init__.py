from ._anvil_designer import ItemSyntheseTemplateTemplate
from anvil import *

class ItemSyntheseTemplate(ItemSyntheseTemplateTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Récupération valeurs
    ultime = self.item.get("ultime", "")
    typ = self.item.get("type", "")
    total = self.item.get("pct_total_txt", "")

    # Remplissage labels (comme ton template qui marche)
    self.label_ultime.text = ultime
    self.label_type.text = typ
    self.label_total.text = total

  def btn_voir_chemins_click(self, **event_args):
    # Event custom OK (x-...)
    self.parent.raise_event("x-select-ultime", ultime=self.item.get("ultime"))


