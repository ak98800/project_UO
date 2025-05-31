from ._anvil_designer import PageFicheParticipationTemplate
from anvil import *
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.server
import anvil.users
from .. import PageDossier




class PageFicheParticipation(PageFicheParticipationTemplate):
  def __init__(self, dossier, nom_societe, **properties):
    self.init_components(**properties)
    self.dossier = dossier
    self.nom_societe = nom_societe


    # ✅ Import dynamique
    from ...NavigationBar import NavigationBar
    self.header_panel.role = "sticky-header"
    self.content_panel.role = "scrollable-content"
    self.navigation_bar_panel.clear()
    self.navigation_bar_panel.add_component(NavigationBar())

    # 🔐 Authentification
    self.user = anvil.users.get_user()
    self.profil = anvil.server.call("get_profil", self.user)

    # En-tête de la fiche
    self.nom_societe_label.text = f"Société : {self.nom_societe}"
    self.total_parts_textbox.text = ""
    self.groupe_textbox.text = ""
    self.sous_groupe_textbox.text = ""

    # Placeholder visuel
    self.statut_label.text = "⚠️ Données à compléter"
    self.statut_label.foreground = "orange"

    # Chargement initial
    self.recharger_lignes()
    self.charger_infos_societe()

  def recharger_lignes(self):
    participations = anvil.server.call(
      "get_participations_pour_societe",
      self.dossier["id"],
      self.nom_societe
    )

    for p in participations:
      p["dossier"] = self.dossier
      p["societe"] = self.nom_societe
      p["id"] = p.get("id")

    self.repeating_participations.items = participations

    total_pct = sum(p.get("pourcentage", 0) or 0 for p in participations)

    if total_pct == 100:
      self.statut_label.text = f"✅ Structure complète ({total_pct:.1f} %)"
      self.statut_label.foreground = "green"
    elif total_pct < 100:
      self.statut_label.text = f"⚠️ Incomplet ({total_pct:.1f} %)"
      self.statut_label.foreground = "orange"
    else:
      self.statut_label.text = f"❌ Excès ({total_pct:.1f} %)"
      self.statut_label.foreground = "red"

  def charger_infos_societe(self):
    infos = anvil.server.call("get_infos_societe", self.dossier["id"], self.nom_societe)
    if infos:
      self.total_parts_textbox.text = str(infos.get("total_parts") or "")
      self.groupe_textbox.text = infos.get("groupe") or ""
      self.sous_groupe_textbox.text = infos.get("sous_groupe") or ""

  def enregistrer_en_tete_button_click(self, **event_args):
    total = self.total_parts_textbox.text.strip()
    groupe = self.groupe_textbox.text.strip() or None
    sous_groupe = self.sous_groupe_textbox.text.strip() or None
    try:
      anvil.server.call(
        "enregistrer_infos_societe",
        self.dossier["id"],
        self.nom_societe,
        total,
        groupe,
        sous_groupe
      )
      Notification("Informations enregistrées.", style="success").show()
    except Exception as e:
      Notification(str(e), style="danger").show()

  def ajouter_actionnaire_button_click(self, **event_args):
    from .PopupAjouterActionnaire import PopupAjouterActionnaire
    popup = PopupAjouterActionnaire(self.dossier, self.nom_societe)
    popup.set_event_handler("x-actionnaire-ajoute", self._rafraichir_apres_ajout)
    alert(popup, large=True, buttons=[])

  def _rafraichir_apres_ajout(self, **event_args):
    self.recharger_lignes()

  def retour_button_click(self, **event_args):
    open_form(PageDossier(dossier=self.dossier))



  def refresh_fiche_participation(self):
    self.recharger_lignes()
