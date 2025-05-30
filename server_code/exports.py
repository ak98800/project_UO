import anvil.email
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def generer_export_html(nodes, edges):
  import json
  html_code = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Organigramme Interactif</title>
  <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    #mynetwork {{
      width: 100%;
      height: 900px;
      border: 1px solid #ccc;
    }}
    .button-bar {{
      margin-bottom: 10px;
    }}
  </style>
</head>
<body>
  <h2>Organigramme Interactif</h2>
  <div class="button-bar">
    <button onclick="switchToFree()">Vue libre</button>
    <button onclick="switchToVertical()">Vue verticale</button>
    <button onclick="switchToHorizontal()">Vue horizontale</button>
  </div>
  <div id="mynetwork"></div>

  <script>
    const nodes = new vis.DataSet({json.dumps(nodes)});
    const edges = new vis.DataSet({json.dumps(edges)});
    const container = document.getElementById("mynetwork");
    let network = null;

    function renderGraph(layoutOptions) {{
      const data = {{ nodes, edges }};
      const options = {{
        layout: layoutOptions,
        physics: false,
        interaction: {{
          dragView: true,
          zoomView: true,
          dragNodes: true,
          navigationButtons: true
        }},
        nodes: {{
          shape: "ellipse",
          scaling: {{ min: 10, max: 30 }},
          font: {{ size: 12 }}
        }},
        edges: {{
          arrows: "to",
          smooth: false,
          color: {{ color: "#999999" }},
          font: {{ align: "middle", size: 12 }}
        }}
      }};
      network = new vis.Network(container, data, options);
    }}

    function switchToFree() {{
      renderGraph({{ hierarchical: false }});
    }}

    function switchToVertical() {{
      renderGraph({{
        hierarchical: {{
          enabled: true,
          direction: "UD",
          sortMethod: "hubsize",
          levelSeparation: 150,
          nodeSpacing: 150,
          treeSpacing: 300
        }}
      }});
    }}

    function switchToHorizontal() {{
      renderGraph({{
        hierarchical: {{
          enabled: true,
          direction: "LR",
          sortMethod: "hubsize",
          levelSeparation: 150,
          nodeSpacing: 150,
          treeSpacing: 300
        }}
      }});
    }}

    // Initial rendering
    switchToFree();
  </script>
</body>
</html>
"""
  return html_code




