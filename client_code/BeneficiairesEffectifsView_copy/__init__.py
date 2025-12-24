from ._anvil_designer import BeneficiairesEffectifsView_copyTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from ..HTMLTestForm import HTMLTestForm
from collections import defaultdict


class BeneficiairesEffectifsView_copy(BeneficiairesEffectifsView_copyTemplate):
  def __init__(self, dossier, societe_point_depart=None, societe=None, **properties):
    self.init_components(**properties)

    self.dossier = dossier

    # compatible : string ou dict
    if societe_point_depart:
      self.societe_point_depart = societe_point_depart
    elif isinstance(societe, dict) and societe.get("name"):
      self.societe_point_depart = societe["name"]
    else:
      self.societe_point_depart = None

    self._nodes = []
    self._edges = []

    self.label_welcome.text = f"Bienvenue, {anvil.users.get_user()['email']}"
    self.dropdown_dossier.visible = False

    self.form_test = HTMLTestForm()
    self.panel.add_component(self.form_test)

    self.dropdown_direction.items = [
      ("Verticale (haut → bas)", "UD"),
      ("Horizontale (gauche → droite)", "LR"),
    ]
    self.dropdown_direction.selected_value = "UD"

  def _fmt_pct(self, p):
    try:
      p = float(p or 0)
    except:
      p = 0.0
    # 2 décimales seulement si nécessaire
    if abs(p - round(p)) < 1e-9:
      return f"{int(round(p))}%"
    return f"{p:.2f}".replace(".", ",") + "%"

  def btn_afficher_graph_click(self, **event_args):
    self._build_graph()
    self._call_js()

  def _build_graph(self):
    if not self.societe_point_depart:
      alert("Aucune société cible.")
      self._nodes, self._edges = [], []
      return

    dossier_name = self.dossier["name"]
    cible = self.societe_point_depart

    relations = anvil.server.call("get_ultimes_interets", dossier_name, cible)

    noms_uniques = set()
    edges = []
    types = {}
    degree_map = defaultdict(int)

    # On force la cible à être dans les nodes
    noms_uniques.add(cible)

    for ultime, societe_cible, pct_total, type_ultime in relations:
      noms_uniques.update([ultime, societe_cible])
      types[ultime] = type_ultime or "PM"
      degree_map[ultime] += 1
      degree_map[societe_cible] += 1

      pct_txt = self._fmt_pct(pct_total)

      edges.append(
        {
          "from": ultime,
          "to": societe_cible,
          "label": pct_txt,
          "title": f"{ultime} → {societe_cible} : {pct_txt}",
          "font": {"align": "middle", "size": 12},
        }
      )

    nodes = []
    for name in noms_uniques:
      # Couleur PP/PM + on laisse le halo de la cible au JS via selectedName
      node_color = "#FFD700" if types.get(name) == "PP" else "#D2E5FF"
      if name == cible:
        node_color = "#D2E5FF"  # la cible sera surlignée côté JS (halo), pas besoin de casser le thème

      nodes.append(
        {
          "id": name,
          "label": name,
          "title": name,
          "color": node_color,
          "value": max(degree_map.get(name, 1), 1),
        }
      )

    self._nodes = nodes
    self._edges = edges

  def _call_js(self):
    direction = self.dropdown_direction.selected_value or "UD"
    selected = self.societe_point_depart
    self.form_test.call_js("drawGraph", self._nodes, self._edges, direction, selected)

  def btn_export_html_click(self, **event_args):
    self._build_graph()
    html_code = anvil.server.call(
      "generer_export_html", self._nodes, self._edges, self.societe_point_depart
    )
    media = anvil.BlobMedia(
      "text/html", html_code.encode("utf-8"), name="beneficiaires_effectifs.html"
    )
    anvil.media.download(media)

  def btn_afficher_html_click(self, **event_args):
    self._build_graph()
    html_code = anvil.server.call(
      "generer_export_html", self._nodes, self._edges, self.societe_point_depart
    )

    js_script = f"""
      var htmlContent = `{html_code}`;
      var blob = new Blob([htmlContent], {{ type: "text/html" }});
      var url = URL.createObjectURL(blob);
      window.open(url, "_blank");
    """
    anvil.js.call("eval", js_script)
