import anvil.server
from datetime import datetime
from collections import defaultdict

from . import graph
from . import exports

def _relations_to_nodes_edges(relations):
  """
  relations: list of tuples (actionnaire, societe, pourcentage, type_act)
  -> nodes/edges au format attendu par exports.generer_export_html(...)
  """
  noms_uniques, edges, types_actionnaires, degree_map = set(), [], {}, defaultdict(int)

  for actionnaire, societe, pourcentage, type_act in relations:
    pourcentage = pourcentage or 0
    noms_uniques.update([actionnaire, societe])
    types_actionnaires[actionnaire] = type_act or "PM"
    degree_map[actionnaire] += 1

    edges.append({
      "from": actionnaire,
      "to": societe,
      "label": f"{pourcentage}%",
      "title": f"{actionnaire} → {societe} : {pourcentage}%",
      "font": {"align": "middle", "size": 12}
    })

  nodes = [{
    "id": name,
    "label": name,
    "title": f"{name} (détient {degree_map.get(name, 1)} société(s))",
    "color": "#FFD700" if types_actionnaires.get(name) == "PP" else "#D2E5FF",
    "value": degree_map.get(name, 1)
  } for name in noms_uniques]

  return nodes, edges

def _get_actionnariat_direct_only(dossier_name, societe_cible):
  """
  Renvoie relations (actionnaire -> societe_cible) uniquement (niveau direct).
  On reconstruit depuis graph.get_relations_dossier_typed puis on filtre,
  comme ça tu n'as rien à adapter ailleurs.
  """
  relations_all = graph.get_relations_dossier_typed(dossier_name)  # (actionnaire, societe, pct, type_act)
  return [(a, s, p, t) for (a, s, p, t) in relations_all if s == societe_cible]

@anvil.server.callable
def generate_societe_report_html(dossier_name, societe, options):
  """
  MVP étape 2 : Section Actionnariat réelle (organigramme).
  Le reste reste placeholder pour l'instant.
  """
  # ---- options actionnariat ----
  action_opts = (options or {}).get("actionnariat", {})
  scope = action_opts.get("scope", "direct_indirect")   # "direct" ou "direct_indirect"
  display = action_opts.get("display", "org")           # "org" / "org_table" / "table"

  # ---- construire le HTML Actionnariat ----
  actionnariat_org_html = ""
  actionnariat_table_html = ""

  if display in ("org", "org_table"):
    if scope == "direct":
      relations = _get_actionnariat_direct_only(dossier_name, societe)
    else:
      # direct + indirect jusqu'aux sommets = montante
      relations = graph.get_relations_montantes(dossier_name, societe)

    nodes, edges = _relations_to_nodes_edges(relations)
    actionnariat_org_html = exports.generer_export_html(nodes, edges, societe)

  if display in ("table", "org_table"):
    # placeholder étape suivante
    actionnariat_table_html = "<p><i>(Tableau actionnariat : étape suivante)</i></p>"

  # ---- page HTML ----
  now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  html = f"""
  <html>
    <head>
      <meta charset="utf-8">
      <title>Rapport {societe}</title>
      <style>
        body {{ font-family: Arial, sans-serif; font-size: 14px; }}
        h1 {{ margin: 0; }}
        .meta {{ margin-top: 6px; color: #555; }}
        .section {{ margin-top: 22px; }}
        .box {{ border: 1px solid #ddd; padding: 12px; border-radius: 8px; }}
      </style>
    </head>
    <body>
      <h1>Rapport Société</h1>
      <div class="meta">
        <div><b>Dossier :</b> {dossier_name}</div>
        <div><b>Société :</b> {societe}</div>
        <div><b>Généré le :</b> {now_str}</div>
      </div>

      <div class="section">
        <h2>1) Actionnariat</h2>
        <div class="box">
          {actionnariat_org_html}
          {actionnariat_table_html}
        </div>
      </div>

      <div class="section">
        <h2>2) Sections à venir</h2>
        <p><i>(Descendante / Montante / Bénéficiaires effectifs / Annexes)</i></p>
      </div>
    </body>
  </html>
  """
  return html
