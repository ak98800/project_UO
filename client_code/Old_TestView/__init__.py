from ._anvil_designer import Old_TestViewTemplate
from anvil import *
import anvil.js
import anvil.js.window

class Old_TestView(Old_TestViewTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.inject_visjs_script()

  def inject_visjs_script(self):
    inject_code = """
      if (!window.visLoaded) {
        var script = document.createElement('script');
        script.src = "https://unpkg.com/vis-network/standalone/umd/vis-network.min.js";
        script.onload = function() {
          window.visLoaded = true;
          window.drawGraph = function(data) {
            var nodes = new vis.DataSet(data.nodes);
            var edges = new vis.DataSet(data.edges);
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
          };
        };
        document.head.appendChild(script);
      }
    """
    anvil.js.window.eval(inject_code)

  def timer_1_tick(self, **event_args):
    draw_code = """
      if (window.visLoaded && typeof drawGraph === 'function') {
        drawGraph({
          nodes: [
            {id: 1, label: "Départ"},
            {id: 2, label: "Étape 1"},
            {id: 3, label: "Étape 2"}
          ],
          edges: [
            {from: 1, to: 2},
            {from: 2, to: 3}
          ]
        });
      } else {
        alert("vis.js n’est pas encore chargé");
      }
    """
    anvil.js.window.eval(draw_code)
