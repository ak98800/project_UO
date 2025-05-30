import anvil.server
from anvil.tables import app_tables

@anvil.server.callable
def get_dossiers_disponibles():
  # Extraire les noms des dossiers à partir du lien 'folder'
  rows = app_tables.participations.search()
  dossiers = set()
  for row in rows:
    dossier = row['folder']
    if dossier:
      dossiers.add(dossier['name'])  # ou dossier['name'] selon ta table folders
  return sorted(dossiers)


@anvil.server.callable
def get_relations_dossier(nom_dossier):
  # Filtrer les participations liées au dossier sélectionné
  rows = app_tables.participations.search()
  relations = []
  for row in rows:
    dossier = row['folder']
    if dossier and dossier['name'] == nom_dossier:
      actionnaire = row['actionnaire']
      societe = row['societe']
      pourcentage = row['pourcentage'] or 0
      if actionnaire and societe:
        relations.append((actionnaire, societe, pourcentage))
  return relations

@anvil.server.callable
def get_relations_dossier_typed(nom_dossier):
  rows = app_tables.participations.search()
  results = []
  for row in rows:
    folder = row['folder']
    if folder and folder['name'] == nom_dossier:
      actionnaire = row['actionnaire']
      societe = row['societe']
      pourcentage = row['pourcentage'] or 0
      type_actionnaire = row['type_actionnaire'] or "PM"
      if actionnaire and societe:
        results.append((actionnaire, societe, pourcentage, type_actionnaire))
  return results
