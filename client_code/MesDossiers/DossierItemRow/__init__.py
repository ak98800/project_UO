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

  def button_acceder_dossier_click(self, **event_args):
    from ..PageDossier import PageDossier
    open_form(PageDossier, dossier=self.item)

