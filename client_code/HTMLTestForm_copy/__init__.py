from ._anvil_designer import HTMLTestForm_copyTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class HTMLTestForm_copy(HTMLTestForm_copyTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def inject_html(self, html_code):
    print("🔁 HTML injecté dans HTMLTestForm")
    self.html_container.content = html_code
