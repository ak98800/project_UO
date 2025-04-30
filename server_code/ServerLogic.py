import anvil.users
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def enregistrer_profil(user, name, organisation, fonction):
  if not user:
    raise Exception("Utilisateur non authentifié.")
  app_tables.profiles.add_row(
    user=user,
    name=name,
    organisation=organisation,
    fonction=fonction
  )

@anvil.server.callable
def envoyer_email_confirmation():
  anvil.users.send_confirmation_email()
