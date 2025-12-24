import anvil.email
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def generer_export_html(nodes, edges, cible=None):
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
    const cible = {json.dumps(cible)};

    // ✅ DataSets identiques à ton code d'origine
    const nodes = new vis.DataSet({json.dumps(nodes)});
    const edges = new vis.DataSet({json.dumps(edges)});
    const container = document.getElementById("mynetwork");
    let network = null;

    // ✅ PATCH MINIMAL : style cible
    function applyCibleStyle() {{
      if (!cible) return;

      // récupère le node
      const n = nodes.get(cible);
      if (!n) return;

      // met en évidence sans casser le reste
      nodes.update({{
        id: cible,
        color: {{ background: "#FF6B00", border: "#FFFFFF" }},
        borderWidth: 6,
        borderWidthSelected: 10,
        font: {{ size: 16, bold: true, color: "#000000" }}
      }});
    }}

    function renderGraph(layoutOptions) {{
      // ✅ toujours le même data
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
      applyCibleStyle();
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
      applyCibleStyle();
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
      applyCibleStyle();
    }}

    // Initial rendering
    applyCibleStyle();
    switchToFree();
  </script>
</body>
</html>
"""
  return html_code





