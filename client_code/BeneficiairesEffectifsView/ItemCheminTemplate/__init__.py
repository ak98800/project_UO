from ._anvil_designer import ItemCheminTemplateTemplate
from anvil import *

class ItemCheminTemplate(ItemCheminTemplateTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    ultime = self.item.get("ultime", "")
    pct = self.item.get("pct_path_txt", "")
    path_txt = self.item.get("path_txt", "")
    calc = self.item.get("calc", "")

    self.label_ultime.text = ultime
    self.label_pct.text = pct
    self.label_path.text = path_txt
    self.label_calc.text = calc


