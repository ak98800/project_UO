from ._anvil_designer import VueDescendateViewTemplate
from anvil import *
import anvil.users
import anvil.server
from ..HTMLTestForm import HTMLTestForm
from collections import defaultdict


class VueDescendateView(VueDescendateViewTemplate):
  def __init__(self, dossier, societe_point_depart=None, **properties):
    self.init_components(**properties)
    self.dossier = dossier
    self.societe_point_depart = societe_point_depart

    self._nodes = []
    self._edges = []

    self.label_welcome.text = f"Bienvenue, {anvil.users.get_user()['email']}"
    self.dropdown_dossier.visible = False

    self.form_test = HTMLTestForm()
    self.panel.add_component(self.form_test)

    self.dropdown_direction.items = [
      ("Verticale (haut → bas)", "UD"),
      ("Horizontale (gauche → droite)", "LR")
    ]
    self.dropdown_direction.selected_value = "UD"

  def btn_afficher_graph_click(self, **event_args):
    self._afficher_organigramme()
    self._call_js()

  def _afficher_organigramme(self):
    dossier_name = self.dossier['name']

    if self.societe_point_depart:
      relations = anvil.server.call('get_relations_descendantes', dossier_name, self.societe_point_depart)
    else:
      relations = anvil.server.call('get_relations_dossier_typed', dossier_name)

    noms_uniques, edges, types_actionnaires, degree_map = set(), [], {}, defaultdict(int)

    for actionnaire, societe, pourcentage, type_act in relations:
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

    self._nodes = nodes
    self._edges = edges

  def _call_js(self):
    direction = self.dropdown_direction.selected_value or "UD"
    selected = self.societe_point_depart
    # drawGraph(nodes, edges, direction, selectedName)
    self.form_test.call_js("drawGraph", self._nodes, self._edges, direction, selected)

  def form_show(self, **event_args):
    pass

  def btn_export_html_click(self, **event_args):
    dossier_name = self.dossier['name']
    if self.societe_point_depart:
      relations = anvil.server.call('get_relations_descendantes', dossier_name, self.societe_point_depart)
    else:
      relations = anvil.server.call('get_relations_dossier_typed', dossier_name)
  
    noms_uniques, edges, types_actionnaires, degree_map = set(), [], {}, defaultdict(int)
  
    for actionnaire, societe, pourcentage, type_act in relations:
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
  
    html_code = anvil.server.call('generer_export_html', nodes, edges, self.societe_point_depart)
    media = anvil.BlobMedia("text/html", html_code.encode("utf-8"), name="organigramme_interactif.html")
    anvil.media.download(media)
  
  
  def btn_afficher_html_click(self, **event_args):
    dossier_name = self.dossier['name']
    if self.societe_point_depart:
      relations = anvil.server.call('get_relations_descendantes', dossier_name, self.societe_point_depart)
    else:
      relations = anvil.server.call('get_relations_dossier_typed', dossier_name)
  
    noms_uniques, edges, types_actionnaires, degree_map = set(), [], {}, defaultdict(int)
  
    for actionnaire, societe, pourcentage, type_act in relations:
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
  
    html_code = anvil.server.call('generer_export_html', nodes, edges, self.societe_point_depart)
  
    js_script = f"""
      var htmlContent = `{html_code}`;
      var blob = new Blob([htmlContent], {{ type: "text/html" }});
      var url = URL.createObjectURL(blob);
      window.open(url, "_blank");
    """
    anvil.js.call("eval", js_script)
