from ._anvil_designer import VueSyntheseViewTemplate
from anvil import *
from ..HTMLTestForm import HTMLTestForm
from anvil.tables import app_tables
import anvil.server

from ..NavigationBar import NavigationBar  # Assure-toi que ce fichier existe

class VueSyntheseView(VueSyntheseViewTemplate):
  def __init__(self, nom_dossier=None, **properties):
    self.init_components(**properties)
    
    # ✅ Appliquer le rôle sticky au header
    self.header_panel.role = "sticky-header"

    # ✅ Appliquer le rôle scrollable au contenu
    self.content_panel.role = "scrollable-content"

    # ✅ Ajouter la barre de navigation à gauche
    self.navigation_bar_panel.clear()
    self.navigation_bar_panel.add_component(NavigationBar())

    # ✅ Message de bienvenue
    user = anvil.users.get_user()
    self.label_welcome.text = f"Bienvenue, {user['email']}" if user else "Bienvenue !"

    # Récupérer les dossiers
    self.dossiers_disponibles = anvil.server.call('get_dossiers_disponibles')
    self.dropdown_dossier.items = self.dossiers_disponibles

    # Ajouter le HTMLTestForm au layout
    self.form_test = HTMLTestForm()
    self.panel.add_component(self.form_test)

    self.dropdown_direction.items = [
      ("Verticale (haut → bas)", "UD"),
      ("Horizontale (gauche → droite)", "LR")
    ]
    self.dropdown_direction.selected_value = "UD"  # Par défaut


  def btn_afficher_graph_click(self, **event_args):
    nom_dossier = self.dropdown_dossier.selected_value
    direction = self.dropdown_direction.selected_value or "UD"
  
    if not nom_dossier:
      alert("Veuillez sélectionner un dossier.")
      return
  
    relations = anvil.server.call('get_relations_dossier_typed', nom_dossier)
  
    noms_uniques = set()
    edges = []
    types_actionnaires = {}
    from collections import defaultdict
    degree_map = defaultdict(int)
  
    for actionnaire, societe, pourcentage, type_act in relations:
      noms_uniques.add(actionnaire)
      noms_uniques.add(societe)
      types_actionnaires[actionnaire] = type_act or "PM"
      degree_map[actionnaire] += 1
  
      edges.append({
        "from": actionnaire,
        "to": societe,
        "label": f"{pourcentage}%",
        "title": f"{actionnaire} → {societe} : {pourcentage}%",
        "font": {"align": "middle", "size": 12}
      })
  
    nodes = []
    for name in noms_uniques:
      color = "#FFD700" if types_actionnaires.get(name) == "PP" else "#D2E5FF"
      value = degree_map.get(name, 1)
      nodes.append({
        "id": name,
        "label": name,
        "title": f"{name} (détient {value} société(s))",
        "color": color,
        "value": value
      })
  
    # Appel JavaScript avec la direction choisie
    self.form_test.call_js("drawGraph", nodes, edges, direction)


  def btn_export_html_click(self, **event_args):
    """Génère et télécharge l'organigramme en fichier HTML interactif"""
  
    nom_dossier = self.dropdown_dossier.selected_value
    if not nom_dossier:
      alert("Veuillez sélectionner un dossier.")
      return
  
      # Appel serveur pour récupérer nodes et edges
    relations = anvil.server.call('get_relations_dossier_typed', nom_dossier)
  
    noms_uniques = set()
    edges = []
    types_actionnaires = {}
    from collections import defaultdict
    degree_map = defaultdict(int)
  
    for actionnaire, societe, pourcentage, type_act in relations:
      noms_uniques.add(actionnaire)
      noms_uniques.add(societe)
      types_actionnaires[actionnaire] = type_act or "PM"
      degree_map[actionnaire] += 1
  
      edges.append({
        "from": actionnaire,
        "to": societe,
        "label": f"{pourcentage}%",
        "title": f"{actionnaire} → {societe} : {pourcentage}%",
        "font": {"align": "middle", "size": 12}
      })
  
    nodes = []
    for name in noms_uniques:
      color = "#FFD700" if types_actionnaires.get(name) == "PP" else "#D2E5FF"
      value = degree_map.get(name, 1)
      nodes.append({
        "id": name,
        "label": name,
        "title": f"{name} (détient {value} société(s))",
        "color": color,
        "value": value
      })
  
      # Appel du serveur pour générer le HTML
    html_code = anvil.server.call('generer_export_html', nodes, edges)
  
    # Conversion en média et téléchargement
    media = anvil.BlobMedia("text/html", html_code.encode("utf-8"), name="organigramme_interactif.html")
    anvil.media.download(media)
