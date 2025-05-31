from ._anvil_designer import PageAnalyserDossierTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.users

from ..NavigationBar import NavigationBar


class PageAnalyserDossier(PageAnalyserDossierTemplate):
  def __init__(self, dossier=None, **properties):
    self.init_components(**properties)

    self.user = anvil.users.get_user()
    self.profil = anvil.server.call("get_profil", self.user)

    # Appliquer les rôles UI
    self.header_panel.role = "sticky-header"
    self.content_panel.role = "scrollable-content"
    self.navigation_bar_panel.clear()
    self.navigation_bar_panel.add_component(NavigationBar())

    self.label_welcome.text = f"Bienvenue, {self.user['email']}" if self.user else "Bienvenue !"

    # 🔁 Chargement des dossiers
    self.dossiers = anvil.server.call("get_dossiers", self.profil["organisation"])
    self.dropdown_dossiers.items = [(d["name"], d) for d in self.dossiers]

    # ✅ Sélectionner automatiquement le dossier si passé en paramètre
    if dossier:
      self.dossier = dossier
      self.dropdown_dossiers.selected_value = dossier
      self._afficher_organigramme()
    else:
      self.dossier = None

  def charger_dossiers_utilisateur(self):
    try:
      user = anvil.users.get_user()
      if not user:
        raise Exception("Utilisateur non connecté.")

      # 🔐 Récupérer le profil et l'organisation
      profil = anvil.server.call("get_profil", user)
      organisation = profil["organisation"]

      # 📦 Charger les dossiers accessibles
      dossiers = anvil.server.call("get_dossiers", organisation)
      self.dropdown_dossiers.items = [(d["name"], d) for d in dossiers]

      # Si un dossier était déjà passé, le sélectionner automatiquement
      if self.dossier:
        for label, d in self.dropdown_dossiers.items:
          if d["id"] == self.dossier["id"]:
            self.dropdown_dossiers.selected_value = d
            break

    except Exception as e:
      Notification(f"Erreur chargement des dossiers : {e}", style="danger").show()

  def dropdown_dossiers_change(self, **event_args):
    dossier = self.dropdown_dossiers.selected_value
    if dossier:
      self.dossier = dossier
      Notification(f"Dossier sélectionné : {dossier['name']}", style="info").show()
      # Tu peux ici appeler une fonction pour afficher le contenu par défaut (organigramme général)


  def _afficher_organigramme(self):
    self.clear_zone_contenu()
    # TODO : ajouter ici le composant OrganigrammeView ou équivalent
    self.zone_contenu.add_component(Label(text="Organigramme à venir..."))

  def clear_zone_contenu(self):
    self.zone_contenu.clear()
