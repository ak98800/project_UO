import anvil.email
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable(require_user=True)
def calculate_percentage_of(number, total_number):
  percentage = (int(number) / int(total_number)) * 100
  return percentage
