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
  """

  def __init__(self, dossier=None, societe=None, **properties):
    self.init_components(**properties)

    self.dossier = dossier
    self.societe = societe
    self._current_html = None

    # --- Affichage contexte (si tu as ces labels) ---
    if hasattr(self, "label_dossier"):
      self.label_dossier.text = dossier["name"] if dossier else ""
    if hasattr(self, "label_societe"):
      self.label_societe.text = societe or ""

    # --- Defaults (MVP) ---
    # Actionnariat: direct + indirect jusqu'aux sommets, org+table
    self._set_selected_value_safe("rg_action_scope", "direct_indirect")
    self._set_selected_value_safe("rg_action_display", "act_org_table")

    # Descendante / Montante / BE: enabled par défaut selon ton choix
    self._set_checked_safe("cb_desc", False)
    self._set_checked_safe("cb_mont", True)
    self._set_checked_safe("cb_be", True)

    # Display defaults (values doivent être uniques dans Anvil -> préfixées)
    self._set_selected_value_safe("rg_desc_display", "desc_org")
    self._set_selected_value_safe("rg_mont_display", "mont_org")
    self._set_selected_value_safe("rg_be_display", "be_org_table")

    # BE options
    self._set_checked_safe("cb_be_25", False)            # au départ: totalité
    self._set_checked_safe("cb_be_paths", False)         # annexe chemins off
    self._set_checked_safe("cb_be_calc_table", False)    # table chemin de calcul off

    # Pas de preview dans Anvil (scripts neutralisés) -> on ouvre un onglet
    # Donc on laisse btn_download_html actif directement (si dossier+societe OK)
    if hasattr(self, "btn_download_html"):
      self.btn_download_html.enabled = bool(self.dossier and self.societe)

    self._sync_enabled_states()

  # -----------------------
  # Helpers safe UI
  # -----------------------
  def _set_selected_value_safe(self, component_name, value):
    c = getattr(self, component_name, None)
    if c is not None:
      try:
        c.selected_value = value
      except Exception:
        pass

  def _set_checked_safe(self, component_name, checked):
    c = getattr(self, component_name, None)
    if c is not None:
      try:
        c.checked = checked
      except Exception:
        pass

  def _get_selected_value_safe(self, component_name, default=None):
    c = getattr(self, component_name, None)
    if c is None:
      return default
    try:
      return c.selected_value
    except Exception:
      return default

  def _get_checked_safe(self, component_name, default=False):
    c = getattr(self, component_name, None)
    if c is None:
      return default
    try:
      return bool(c.checked)
    except Exception:
      return default

  def _enable_safe(self, component_name, enabled: bool):
    c = getattr(self, component_name, None)
    if c is not None:
      try:
        c.enabled = enabled
      except Exception:
        pass

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
  # UX minimal: enable/disable
  # -----------------------
  def _sync_enabled_states(self):
    desc_on = self._get_checked_safe("cb_desc", False)
    mont_on = self._get_checked_safe("cb_mont", False)
    be_on = self._get_checked_safe("cb_be", False)

    self._enable_safe("rg_desc_display", desc_on)
    self._enable_safe("rg_mont_display", mont_on)
    self._enable_safe("rg_be_display", be_on)

    self._enable_safe("cb_be_25", be_on)
    self._enable_safe("cb_be_paths", be_on)
    self._enable_safe("cb_be_calc_table", be_on)

    if not be_on:
      self._set_checked_safe("cb_be_25", False)
      self._set_checked_safe("cb_be_paths", False)
      self._set_checked_safe("cb_be_calc_table", False)

  # -----------------------
  # Events (connecte-les dans le designer)
  # -----------------------
  def cb_desc_change(self, **event_args):
    self._sync_enabled_states()

  def cb_mont_change(self, **event_args):
    self._sync_enabled_states()

  def cb_be_change(self, **event_args):
    self._sync_enabled_states()

  # -----------------------
  # Build options dict
  # -----------------------
  def _build_options(self):
    action_scope = self._get_selected_value_safe("rg_action_scope", "direct_indirect")
    action_display_raw = self._get_selected_value_safe("rg_action_display", "act_org")
    action_display = self._normalize_display(action_display_raw)

    desc_enabled = self._get_checked_safe("cb_desc", False)
    mont_enabled = self._get_checked_safe("cb_mont", False)
    be_enabled = self._get_checked_safe("cb_be", False)

    desc_display = self._normalize_display(self._get_selected_value_safe("rg_desc_display", "desc_org"))
    mont_display = self._normalize_display(self._get_selected_value_safe("rg_mont_display", "mont_org"))
    be_display = self._normalize_display(self._get_selected_value_safe("rg_be_display", "be_org"))

    return {
      "actionnariat": {"scope": action_scope, "display": action_display},
      "descendante": {"enabled": desc_enabled, "display": desc_display},
      "montante": {"enabled": mont_enabled, "display": mont_display},
      "be": {
        "enabled": be_enabled,
        "threshold_25": self._get_checked_safe("cb_be_25", False),
        "include_paths": self._get_checked_safe("cb_be_paths", False),
        "include_calc_table": self._get_checked_safe("cb_be_calc_table", False),
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
