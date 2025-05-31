from ._anvil_designer import OrganigrammeViewv1Template
from anvil import *
import anvil.users
import anvil.server
from ..HTMLTestForm import HTMLTestForm
from collections import defaultdict


class OrganigrammeViewv1(OrganigrammeViewv1Template):
  def __init__(self, dossier, **properties):
    self.init_components(**properties)
    self.dossier = dossier

    self._nodes = []
    self._edges = []

    # UI setup
    self.header_panel.role = "sticky-header"
    self.content_panel.role = "scrollable-content"
    self.label_welcome.text = f"Bienvenue, {anvil.users.get_user()['email']}"

    # Supprimer la sélection manuelle de dossier
    self.dropdown_dossier.visible = False
    self.btn_afficher_graph.visible = False  # 🔒 bouton masqué

    # Composant HTML avec vis.js
    self.form_test = HTMLTestForm()
    self.panel.add_component(self.form_test)

    # Direction du graphe
    self.dropdown_direction.items = [
      ("Verticale (haut → bas)", "UD"),
      ("Horizontale (gauche → droite)", "LR")
    ]
    self.dropdown_direction.selected_value = "UD"

    # Connecter l'événement "form_show" au chargement visuel
    self.set_event_handler("show", self.form_show)

    # Charger les données du graphe
    self._afficher_organigramme()

  def form_show(self, **event_args):
    """Appelé lorsque le formulaire est visible → on peut maintenant appeler JS"""
    if self._nodes and self._edges:
      direction = self.dropdown_direction.selected_value or "UD"
      self.form_test.call_js("drawGraph", self._nodes, self._edges, direction)

  def _afficher_organigramme(self):
    """Charge les données de relations et stocke nodes/edges"""
    dossier_name = self.dossier['name']
    direction = self.dropdown_direction.selected_value or "UD"
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

    # On stocke pour affichage lors du show()
    self._nodes = nodes
    self._edges = edges

  def btn_afficher_graph_click(self, **event_args):
    """(Plus utilisé) Forcer l'affichage manuellement si besoin"""
    self._afficher_organigramme()
    self.call_js_later()

  def call_js_later(self):
    """Utilisé après clic bouton pour forcer l'affichage du graphe JS"""
    if self._nodes and self._edges:
      direction = self.dropdown_direction.selected_value or "UD"
      self.form_test.call_js("drawGraph", self._nodes, self._edges, direction)

  def btn_export_html_click(self, **event_args):
    """Génère et télécharge un fichier HTML interactif"""
    dossier_name = self.dossier['name']
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

    html_code = anvil.server.call('generer_export_html', nodes, edges)
    media = anvil.BlobMedia("text/html", html_code.encode("utf-8"), name="organigramme_interactif.html")
    anvil.media.download(media)
