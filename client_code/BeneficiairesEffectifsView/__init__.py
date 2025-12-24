from ._anvil_designer import BeneficiairesEffectifsViewTemplate
from anvil import *
import anvil.users
import anvil.server
from ..HTMLTestForm import HTMLTestForm

from .ItemSyntheseTemplate import ItemSyntheseTemplate
from .ItemCheminTemplate import ItemCheminTemplate


class BeneficiairesEffectifsView(BeneficiairesEffectifsViewTemplate):
  def __init__(self, dossier, societe_point_depart=None, societe=None, **properties):
    self.init_components(**properties)

    self.dossier = dossier

    # cible : string
    if societe_point_depart:
      self.societe_point_depart = societe_point_depart
    elif isinstance(societe, dict) and societe.get("name"):
      self.societe_point_depart = societe["name"]
    else:
      self.societe_point_depart = None

    self._nodes = []
    self._edges = []
    self._paths_all = []
    self._paths_filtered = []
    self._synthese = []

    # Header
    try:
      self.label_welcome.text = f"Bienvenue, {anvil.users.get_user()['email']}"
    except:
      self.label_welcome.text = "Bienvenue"
    self.dropdown_dossier.visible = False

    # Graph
    self.form_test = HTMLTestForm()
    self.panel.add_component(self.form_test)

    # Direction
    self.dropdown_direction.items = [
      ("Verticale (haut → bas)", "UD"),
      ("Horizontale (gauche → droite)", "LR")
    ]
    self.dropdown_direction.selected_value = "UD"

    # ✅ CONNECTER LES REPEATING PANELS
    self.rp_synthese.item_template = ItemSyntheseTemplate
    self.rp_paths.item_template = ItemCheminTemplate

    # ✅ EVENT custom (Anvil => x-...)
    self.rp_synthese.set_event_handler("x-select-ultime", self._on_select_ultime)

    # ✅ FORCER VISIBILITÉ / PLACE
    self.rp_synthese.visible = True
    self.rp_paths.visible = True
    # évite les panels "écrasés" si layout mal réglé
    try:
      self.rp_synthese.height = "250px"
      self.rp_paths.height = "350px"
    except:
      pass

    # ✅ DEBUG layout
    print("DEBUG RP synth visible?", self.rp_synthese.visible, "parent=", type(self.rp_synthese.parent).__name__)
    print("DEBUG RP paths visible?", self.rp_paths.visible, "parent=", type(self.rp_paths.parent).__name__)

    # ✅ AUTO LOAD pour test (tu peux enlever après)
    self._build_be()
    self._call_js()
    self._refresh_tables()

  def _fmt_pct(self, p):
    try:
      p = float(p or 0)
    except:
      p = 0.0
    if abs(p - round(p)) < 1e-9:
      return f"{int(round(p))}%"
    return f"{p:.2f}".replace(".", ",") + "%"

  def btn_afficher_graph_click(self, **event_args):
    self._build_be()
    self._call_js()
    self._refresh_tables()

  def _build_be(self):
    if not self.societe_point_depart:
      alert("Aucune société cible.")
      self._nodes, self._edges = [], []
      self._paths_all, self._paths_filtered, self._synthese = [], [], []
      return

    dossier_name = self.dossier["name"]
    cible = self.societe_point_depart

    # 1) chemins complets
    paths = anvil.server.call("get_be_paths", dossier_name, cible)
    self._paths_all = paths
    self._paths_filtered = list(paths)

    print("DEBUG get_be_paths:", len(paths), "cible=", cible, "dossier=", dossier_name)

    # 2) synthèse
    agg = {}
    for row in paths:
      ultime = row.get("ultime")
      t = row.get("type", "PM")
      pct = float(row.get("pct_path") or 0.0)
      depth = int(row.get("depth") or 0)

      if ultime not in agg:
        agg[ultime] = {
          "ultime": ultime,
          "type": t,
          "pct_direct": 0.0,
          "pct_indirect": 0.0,
          "pct_total": 0.0,
          "nb_chemins": 0
        }

      agg[ultime]["pct_total"] += pct
      agg[ultime]["nb_chemins"] += 1
      if depth == 1:
        agg[ultime]["pct_direct"] += pct
      else:
        agg[ultime]["pct_indirect"] += pct

    synthese = list(agg.values())
    synthese.sort(key=lambda x: -float(x.get("pct_total") or 0.0))
    self._synthese = synthese

    print("DEBUG synthese:", len(self._synthese))

    # 3) graph ultimes -> cible
    noms_uniques = set([cible])
    edges = []
    types = {}

    for s in synthese:
      ultime = s["ultime"]
      types[ultime] = s.get("type", "PM")
      noms_uniques.add(ultime)

      pct_txt = self._fmt_pct(s["pct_total"])
      edges.append({
        "from": ultime,
        "to": cible,
        "label": pct_txt,
        "title": f"{ultime} → {cible} : {pct_txt}",
        "font": {"align": "middle", "size": 12}
      })

    nodes = []
    for name in noms_uniques:
      node_color = "#FFD700" if types.get(name) == "PP" else "#D2E5FF"
      nodes.append({
        "id": name,
        "label": name,
        "title": name,
        "color": node_color,
        "value": 5
      })

    self._nodes = nodes
    self._edges = edges

  def _call_js(self):
    direction = self.dropdown_direction.selected_value or "UD"
    selected = self.societe_point_depart
    self.form_test.call_js("drawGraph", self._nodes, self._edges, direction, selected)

  def _refresh_tables(self):
    print("DEBUG refresh_tables synth:", len(self._synthese), "paths:", len(self._paths_filtered))

    # ✅ remplir synthèse
    synth_items = []
    for s in self._synthese:
      synth_items.append({
        **s,
        "pct_direct_txt": self._fmt_pct(s.get("pct_direct")),
        "pct_indirect_txt": self._fmt_pct(s.get("pct_indirect")),
        "pct_total_txt": self._fmt_pct(s.get("pct_total")),
      })

    # Reset puis set (force rerender)
    self.rp_synthese.items = []
    self.rp_synthese.items = synth_items

    # ✅ remplir chemins
    path_items = []
    for p in self._paths_filtered:
      path_items.append({
        **p,
        "pct_path_txt": self._fmt_pct(p.get("pct_path")),
        "path_txt": " → ".join(p.get("path") or [])
      })

    self.rp_paths.items = []
    self.rp_paths.items = path_items

    # Force bindings (au cas où)
    try:
      self.rp_synthese.refresh_data_bindings()
      self.rp_paths.refresh_data_bindings()
    except:
      pass

  def _on_select_ultime(self, ultime=None, **event_args):
    if not ultime:
      return
    self._paths_filtered = [p for p in self._paths_all if p.get("ultime") == ultime]
    self._refresh_tables()

  def btn_reset_filter_click(self, **event_args):
    self._paths_filtered = list(self._paths_all)
    self._refresh_tables()

  def checkbox_be_25_change(self, **event_args):
    if self.checkbox_be_25.checked:
      # Filtrer > 25 %
      self.repeating_panel_1.items = [
        be for be in self.be_tous
        if be.get("total_pourcentage", 0) > 25
      ]
    else:
      # Afficher tout
      self.repeating_panel_1.items = self.be_tous

