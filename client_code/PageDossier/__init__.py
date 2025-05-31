from ._anvil_designer import PageDossierTemplate
from anvil import *
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.server
import anvil.users

from ..NavigationBar import NavigationBar  # Assure-toi que ce fichier existe

class PageDossier(PageDossierTemplate):
  def __init__(self, dossier, **properties):
    self.init_components(**properties)
    self.dossier = dossier

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

    # 🔐 Authentification
    self.user = anvil.users.get_user()
    self.profil = anvil.server.call("get_profil", self.user)

    # 🧾 Infos dossier
    self.nom_dossier_label.text = f"Dossier : {dossier['name']}"
    self.email_admin_label.text = dossier["created_by"]["email"]
    self.date_creation_label.text = dossier["created_at"].strftime("%d/%m/%Y")
    self.nb_users_label.text = str(anvil.server.call("get_nombre_utilisateurs_dossier", dossier["id"]))

    # 🎛 Droits
    est_createur = (dossier["created_by"] == self.user)
    self.button_partager.visible = est_createur
    self.button_supprimer.visible = est_createur

    # 📄 Onglet par défaut
    self.participations_button_click()



  def button_retour_click(self, **event_args):
    from ..MesDossiers import MesDossiers
    open_form(MesDossiers())

  def button_partager_click(self, **event_args):
    from ..GestionPartagePage import GestionPartagePage
    open_form(GestionPartagePage(dossier=self.dossier))

  def button_supprimer_click(self, **event_args):
    if confirm("Supprimer ce dossier ? Action irréversible."):
      try:
        anvil.server.call("supprimer_dossier", self.dossier["id"])
        Notification("Dossier supprimé", style="success").show()
        from ..MesDossiers import MesDossiers
        open_form(MesDossiers())
      except Exception as e:
        Notification(f"Erreur : {e}", style="danger").show()

  # 🔁 Chargement de la vue Participations
  def participations_button_click(self, **event_args):
    self.clear_zone_contenu()
    from .ParticipationsViewSynthese import ParticipationsViewSynthese
    synthese = ParticipationsViewSynthese(dossier=self.dossier)
    synthese.set_event_handler("x-afficher-fiche-societe", self._afficher_fiche_societe)
    self.zone_contenu.add_component(synthese)

  def clear_zone_contenu(self):
    self.zone_contenu.clear()

  def _afficher_fiche_societe(self, composant=None, **event_args):
    self.clear_zone_contenu()
    if composant:
      self.zone_contenu.add_component(composant)

  # ✅ Nouveau : bouton ➕ Ajouter une société
  def ajouter_societe_button_click(self, **event_args):
    Notification("Ajouter une société : à implémenter", style="info").show()

  # ✅ Nouveau : bouton 📊 Analyser le dossier

  def analyser_button_click(self, **event_args):
    from ..PageAnalyserDossier import PageAnalyserDossier
    open_form(PageAnalyserDossier(dossier=self.dossier))


