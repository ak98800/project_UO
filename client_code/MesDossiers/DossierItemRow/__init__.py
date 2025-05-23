from ._anvil_designer import DossierItemRowTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class DossierItemRow(DossierItemRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)



  def form_refreshing_data_bindings(self, **event_args):
    dossier = self.item
    self.nom_label.text = dossier['nom']
    self.admin_label.text = dossier['created_by']['email'] if dossier['created_by'] else "?"
    self.nb_users_label.text = str(dossier['nb_users']) if 'nb_users' in dossier else "0"
  
    user = anvil.users.get_user()
    self.button_supprimer.visible = (dossier['created_by'] == user)
    self.button_partager.visible = (dossier['created_by'] == user)  # ✅ Ajout ici



  def button_acceder_dossier_click(self, **event_args):
    from ..PageDossier import PageDossier
    open_form(PageDossier, dossier=self.item)



  
  def button_supprimer_click(self, **event_args):
    if confirm("Voulez-vous vraiment supprimer ce dossier ? Cette action est irréversible."):
      try:
        anvil.server.call("supprimer_dossier", self.item["id"])
        Notification("Dossier supprimé avec succès.", style="success").show()
        self.parent.raise_event("x-reload-dossiers")
      except Exception as e:
        Notification(f"Erreur lors de la suppression : {e}", style="danger").show()


  def button_partager_click(self, **event_args):
    from ..PartagerDossierPopup import PartagerDossierPopup
    alert(PartagerDossierPopup(dossier=self.item), large=True, buttons=[])
    # ✅ Rafraîchir la liste après fermeture de la popup
    self.parent.raise_event("x-reload-dossiers")




  def repeating_dossiers_x_reload_dossiers(self, **event_args):
    self.recharger_dossiers()