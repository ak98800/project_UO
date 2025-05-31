from ._anvil_designer import GestionPartagePageTemplate
from anvil import *
import anvil.server
import anvil.users

from ..NavigationBar import NavigationBar

class GestionPartagePage(GestionPartagePageTemplate):
  def recharger_utilisateurs(self, **event_args):
    try:
      print(f"📤 Appel get_membres_dossier avec folder_id = {self.dossier['id']}")
      membres = anvil.server.call("get_membres_dossier", self.dossier["id"])
      print("📥 Membres reçus :", membres)
      self.utilisateurs_panel.items = membres
    except Exception as e:
      Notification(f"Erreur chargement membres : {e}", style="danger").show()

  def __init__(self, dossier, **properties):
    self.init_components(**properties)
    self.dossier = dossier

    # 🔐 Authentification
    self.user = anvil.users.get_user()
    self.profil = None

    # Mise en page
    self.header_panel.role = "sticky-header"
    self.content_panel.role = "scrollable-content"
    self.navigation_bar_panel.clear()
    self.navigation_bar_panel.add_component(NavigationBar())

    # Lier l’événement de rafraîchissement avant tout
    self.utilisateurs_panel.set_event_handler("x-reload-utilisateurs", self.recharger_utilisateurs)

    if self.user:
      self.label_welcome.text = f"Bienvenue, {self.user['email']}"
      self.recharger_profil()
    else:
      Notification("Utilisateur non connecté.", style="danger").show()
      self.label_welcome.text = "Bienvenue !"

    # Affichage du nom du dossier
    self.nom_dossier_label.text = f"Dossier : {dossier.get('name', 'Nom inconnu')}"

    # Charger les utilisateurs à inviter
    self.utilisateur_dropdown.include_placeholder = True
    self.charger_utilisateurs_organisation()

  def recharger_profil(self):
    try:
      self.profil = anvil.server.call("get_profil", self.user)
      print("📦 Profil reçu :", self.profil)

      if not self.profil:
        Notification("Profil introuvable.", style="danger").show()
      else:
        self.recharger_utilisateurs()
    except Exception as e:
      Notification(f"Erreur lors du chargement du profil : {e}", style="danger").show()

  def charger_utilisateurs_organisation(self):
    try:
      membres = anvil.server.call("lister_utilisateurs_organisation", self.dossier["organisation"])
      utilisateurs_possibles = [
        (f"{m['name']} ({m['user']['email']})", m) for m in membres
        if m["user"] != anvil.users.get_user()
      ]
      self.utilisateur_dropdown.items = utilisateurs_possibles
    except Exception as e:
      Notification(f"Erreur chargement utilisateurs : {e}", style="danger").show()

  def ajouter_button_click(self, **event_args):
    selection = self.utilisateur_dropdown.selected_value
    if not selection:
      Notification("Veuillez choisir un utilisateur.", style="warning").show()
      return

    try:
      result = anvil.server.call("partager_dossier_avec_utilisateur", selection, self.dossier["id"])
      Notification(result, style="success").show()
      self.charger_utilisateurs_organisation()
      self.recharger_utilisateurs()
    except Exception as e:
      Notification(f"Erreur : {e}", style="danger").show()

  def retour_button_click(self, **event_args):
    from ..PageDossier import PageDossier
    open_form(PageDossier(dossier=self.dossier))
