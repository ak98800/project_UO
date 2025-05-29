from ._anvil_designer import HTMLTestFormTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class HTMLTestForm(HTMLTestFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  # ➕ Méthode pour injecter dynamiquement le graphe
  def inject_html(self, html_code):
    self.html_container.content = html_code  # Le composant RichText ou HTML dans le design
