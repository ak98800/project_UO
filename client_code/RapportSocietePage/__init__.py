# client_code/RapportSocietePage/__init__.py

from ._anvil_designer import RapportSocietePageTemplate
from anvil import *
import anvil.server
import anvil.media
import anvil.js


class RapportSocietePage(RapportSocietePageTemplate):
  """
  Page de génération de rapport Société (HTML) - version 1 bouton.
  - Reçoit dossier (row folders) + societe (str)
  - Construit options depuis la UI
  - Appelle server: generate_societe_report_html(dossier_name, societe, options)
  - Au clic sur btn_download_html : ouvre l'aperçu dans un nouvel onglet + télécharge le HTML

  Correctif:
  - Vérifie STRICTEMENT que les composants existent (sinon exception claire)
  - Applique les valeurs par défaut en affectation directe (pas "safe")
  - Puis applique la logique d'activation/désactivation
  """

  def __init__(self, dossier=None, societe=None, **properties):
    self.init_components(**properties)

    self.dossier = dossier
    self.societe = societe
    self._current_html = None

    # ---------- Correctif: vérifier les noms EXACTS ----------
    self._require_components()

    # ---------- Contexte ----------
    if hasattr(self, "label_dossier"):
      self.label_dossier.text = dossier["name"] if dossier else ""
    if hasattr(self, "label_societe"):
      self.label_societe.text = societe or ""

    # ---------- Defaults (MVP "pro") ----------
    # Actionnariat: direct + indirect jusqu'aux sommets, org+table
    self.rg_action_scope.selected_value = "direct_indirect"
    self.rg_action_display.selected_value = "act_org_table"

    # Descendante: OFF par défaut, affichage org par défaut
    self.cb_desc.checked = False
    self.rg_desc_display.selected_value = "desc_org"

    # Montante: ON par défaut, affichage org
    self.cb_mont.checked = True
    self.rg_mont_display.selected_value = "mont_org"

    # BE: ON par défaut, affichage org+table
    self.cb_be.checked = True
    self.rg_be_display.selected_value = "be_org_table"

    # BE options: au départ tout BE, pas d'annexe, pas de table chemin
    self.cb_be_25.checked = False
    self.cb_be_paths.checked = False
    self.cb_be_calc_table.checked = False

    # 1 seul bouton (download + preview nouvel onglet)
    self.btn_download_html.enabled = bool(self.dossier and self.societe)

    # Appliquer cohérence enabled/disabled
    self._sync_enabled_states()

  # -----------------------
  # Correctif: require components
  # -----------------------
  def _require(self, name: str):
    c = getattr(self, name, None)
    if c is None:
      raise Exception(f"Composant manquant ou mauvais nom dans le Designer : {name}")
    return c

  def _require_components(self):
    # Checkboxes
    self._require("cb_desc")
    self._require("cb_mont")
    self._require("cb_be")
    self._require("cb_be_25")
    self._require("cb_be_paths")
    self._require("cb_be_calc_table")

    # RadioGroupPanels
    self._require("rg_action_scope")
    self._require("rg_action_display")
    self._require("rg_desc_display")
    self._require("rg_mont_display")
    self._require("rg_be_display")

    # Button
    self._require("btn_download_html")

  # -----------------------
  # Normalisation display
  # -----------------------
  def _normalize_display(self, v: str) -> str:
    """
    Values préfixées (act_org, desc_org_table, mont_table, be_org, etc.)
    => retourne org / org_table / table
    """
    if not v:
      return "org"
    parts = v.split("_", 1)
    if len(parts) == 2:
      return parts[1]
    return v

  # -----------------------
  # UX minimal: enable/disable + cohérence
  # -----------------------
  def _sync_enabled_states(self):
    desc_on = bool(self.cb_desc.checked)
    mont_on = bool(self.cb_mont.checked)
    be_on = bool(self.cb_be.checked)

    # Radios display enabled only if section enabled
    self.rg_desc_display.enabled = desc_on
    self.rg_mont_display.enabled = mont_on
    self.rg_be_display.enabled = be_on

    # BE sub-options
    self.cb_be_25.enabled = be_on
    self.cb_be_paths.enabled = be_on

    # If BE disabled => force OFF sub-options
    if not be_on:
      self.cb_be_25.checked = False
      self.cb_be_paths.checked = False
      self.cb_be_calc_table.checked = False

    # ✅ table chemin de calcul utile seulement si BE affiche un tableau (table ou org+table)
    if be_on:
      be_display = self._normalize_display(self.rg_be_display.selected_value)
      allow_calc_table = be_display in ("table", "org_table")
      self.cb_be_calc_table.enabled = allow_calc_table
      if not allow_calc_table:
        self.cb_be_calc_table.checked = False
    else:
      self.cb_be_calc_table.enabled = False

  # -----------------------
  # Events (connecte-les dans le designer)
  # -----------------------
  def cb_desc_change(self, **event_args):
    self._sync_enabled_states()

  def cb_mont_change(self, **event_args):
    self._sync_enabled_states()

  def cb_be_change(self, **event_args):
    self._sync_enabled_states()

  def rg_be_display_change(self, **event_args):
    self._sync_enabled_states()

  # -----------------------
  # Build options dict
  # -----------------------
  def _build_options(self):
    action_scope = self.rg_action_scope.selected_value
    action_display = self._normalize_display(self.rg_action_display.selected_value)

    desc_enabled = bool(self.cb_desc.checked)
    mont_enabled = bool(self.cb_mont.checked)
    be_enabled = bool(self.cb_be.checked)

    desc_display = self._normalize_display(self.rg_desc_display.selected_value)
    mont_display = self._normalize_display(self.rg_mont_display.selected_value)
    be_display = self._normalize_display(self.rg_be_display.selected_value)

    return {
      "actionnariat": {"scope": action_scope, "display": action_display},
      "descendante": {"enabled": desc_enabled, "display": desc_display},
      "montante": {"enabled": mont_enabled, "display": mont_display},
      "be": {
        "enabled": be_enabled,
        "threshold_25": bool(self.cb_be_25.checked),
        "include_paths": bool(self.cb_be_paths.checked),
        "include_calc_table": bool(self.cb_be_calc_table.checked),
        "display": be_display
      }
    }

  # -----------------------
  # Single action button
  # -----------------------
  @handle("btn_download_html", "click")
  def btn_download_html_click(self, **event_args):
    if not self.dossier or not self.societe:
      alert("Dossier ou société manquant(e).")
      return

    options = self._build_options()

    html = anvil.server.call(
      "generate_societe_report_html",
      self.dossier["name"],
      self.societe,
      options
    )

    self._current_html = html

    # 1) Aperçu réel dans un nouvel onglet (scripts OK)
    w = anvil.js.window.open("", "_blank")
    w.document.open()
    w.document.write(html)
    w.document.close()

    # 2) Téléchargement du fichier HTML
    filename = f"rapport_{self.societe}.html".replace(" ", "_")
    media = anvil.BlobMedia("text/html", html.encode("utf-8"), name=filename)
    anvil.media.download(media)
