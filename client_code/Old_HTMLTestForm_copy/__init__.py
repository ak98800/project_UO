from ._anvil_designer import Old_HTMLTestForm_copyTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Old_HTMLTestForm_copy(Old_HTMLTestForm_copyTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def inject_html(self, html_code):
    print("🔁 HTML injecté dans HTMLTestForm")
    self.html_container.content = html_code
