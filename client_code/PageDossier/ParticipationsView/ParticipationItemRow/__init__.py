from ._anvil_designer import ParticipationItemRowTemplate
from anvil import *

class ParticipationItemRow(ParticipationItemRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Définir les largeurs de colonnes
    self.row_panel.set_col_widths({
      "col_1": "15%",
      "col_2": "15%",
      "col_3": "10%",
      "col_4": "10%",
      "col_5": "15%",
      "col_6": "15%",
      "col_7": "5%"
    })

    # Remplir la ligne avec les données
    self.row_panel.add_component(Label(text=self.item['societe']), column="col_1")
    self.row_panel.add_component(Label(text=self.item['actionnaire']), column="col_2")
    self.row_panel.add_component(Label(text=f"{self.item['pourcentage']} %"), column="col_3")
    self.row_panel.add_component(Label(text=self.item['type']), column="col_4")
    self.row_panel.add_component(Label(text=self.item['groupe']), column="col_5")
    self.row_panel.add_component(Label(text=self.item['sous_groupe']), column="col_6")
    self.row_panel.add_component(Icon(name="delete_forever", role="danger"), column="col_7")
