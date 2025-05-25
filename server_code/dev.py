import anvil.email
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import io
from datetime import datetime


@anvil.server.callable
def supprimer_participations_dossier(nom_dossier):
  dossier = app_tables.folders.get(name=nom_dossier)
  if not dossier:
    raise Exception(f"Dossier '{nom_dossier}' introuvable.")

  lignes = app_tables.participations.search(folder=dossier)
  for ligne in lignes:
    ligne.delete()

  return "Participations supprimées avec succès."


@anvil.server.callable
def import_test_participations(nom_dossier, fichier_excel):
  dossier = app_tables.folders.get(name=nom_dossier)
  if not dossier:
    raise Exception(f"Dossier '{nom_dossier}' introuvable.")

  # Lecture du fichier Excel
  df = pd.read_excel(
    io.BytesIO(fichier_excel.get_bytes()), 
    header=None, 
    skiprows=1,
    engine="openpyxl"
  )

  for _, row in df.iterrows():
    def clean(val):
      return None if pd.isna(val) else val

    app_tables.participations.add_row(
      folder=dossier,
      societe=clean(row[0]),
      actionnaire=clean(row[1]),
      type_actionnaire=clean(row[2]),
      nb_parts=clean(row[3]),
      total_parts_societe=clean(row[4]),
      pourcentage=clean(row[5]),
      groupe=clean(row[6]),
      sous_groupe=clean(row[7]),
      created_at=datetime.now()  # ✅ ajout de la date actuelle
    )

  return f"Import Excel terminé avec succès. {len(df)} lignes importées."


