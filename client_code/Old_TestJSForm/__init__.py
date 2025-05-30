from ._anvil_designer import Old_TestJSFormTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Old_TestJSForm(Old_TestJSFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Le code HTML+JS complet (avec chargement propre de vis.js)
    html_code = """
    <div id="mynetwork" style="width:100%; height:600px; border:1px solid #ccc;"></div>

    <script>
      // Injecter vis.js dynamiquement
      if (!window.visLoaded) {
        var script = document.createElement('script');
        script.src = "https://unpkg.com/vis-network/standalone/umd/vis-network.min.js";
        script.onload = function() {
          window.visLoaded = true;
          drawGraph();
        };
        document.head.appendChild(script);
      } else {
        drawGraph();
      }

      function drawGraph() {
        var nodes = new vis.DataSet([
          {id: 1, label: "Départ"},
          {id: 2, label: "Étape 1"},
          {id: 3, label: "Étape 2"}
        ]);

        var edges = new vis.DataSet([
          {from: 1, to: 2},
          {from: 2, to: 3}
        ]);

        var container = document.getElementById("mynetwork");

        var options = {
          layout: {
            hierarchical: {
              enabled: true,
              direction: "UD"
            }
          },
          physics: false,
          edges: { arrows: "to" }
        };

        new vis.Network(container, { nodes: nodes, edges: edges }, options);
      }
    </script>
    """

    # Injecter le HTML dans le RichText
    self.rich_text_test.content = html_code
