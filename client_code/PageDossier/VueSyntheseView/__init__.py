from ._anvil_designer import VueSyntheseViewTemplate
from anvil import *
from ...HTMLTestForm import HTMLTestForm  # importer ton test HTML
from anvil.tables import app_tables
import anvil.server

class VueSyntheseView(VueSyntheseViewTemplate):
  def __init__(self, nom_dossier=None, **properties):
    self.init_components(**properties)

    # Charger les dossiers disponibles depuis la table
    self.dossiers_disponibles = anvil.server.call('get_dossiers_disponibles')
    self.dropdown_dossier.items = self.dossiers_disponibles


    # Affichage du contenu de HTMLTestForm dans cette vue
    form_test = HTMLTestForm()
    self.add_component(form_test)

  def btn_afficher_graph_click(self, **event_args):
    nom_dossier = self.dropdown_dossier.selected_value

    if not nom_dossier:
      alert("Veuillez sélectionner un dossier.")
      return

    relations = anvil.server.call('get_relations_dossier', nom_dossier)

    noms_uniques = set()
    edges = []

    for actionnaire, societe, pourcentage in relations:
      noms_uniques.add(actionnaire)
      noms_uniques.add(societe)
      edges.append({
        "from": actionnaire,
        "to": societe,
        "label": f"{pourcentage}%",
        "font": { "align": "middle" }
      })

    nodes = [{"id": name, "label": name} for name in noms_uniques]

    html_code = f"""
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <div id="mynetwork" style="width:100%; height:600px; border:1px solid #ccc; margin-top:20px;"></div>
    <script>
      const nodes = new vis.DataSet({nodes});
      const edges = new vis.DataSet({edges});
      const container = document.getElementById("mynetwork");

      const options = {{
        layout: {{
          hierarchical: {{
            enabled: true,
            direction: "UD"
          }}
        }},
        physics: false,
        edges: {{
          arrows: "to",
          font: {{ align: "horizontal" }}
        }}
      }};

      new vis.Network(container, {{ nodes: nodes, edges: edges }}, options);
    </script>
    """

    # ✅ Injection propre dans HTMLTestForm déjà affiché
    self.form_test.inject_html(html_code)









