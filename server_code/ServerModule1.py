import anvil.email
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def rechercher_dossiers(nom_partiel):
  user = anvil.users.get_user()
  if not nom_partiel.strip():
    return app_tables.folders.search(created_by=user)

  print(f"Recherche côté serveur : {nom_partiel}")  # DEBUG
  return app_tables.folders.search(
    created_by=user,
    name=q.ilike(f"%{nom_partiel}%")
  )
