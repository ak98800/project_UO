import anvil.email
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.server.callable
def supprimer_participations_dossier(nom_dossier):
  dossier = app_tables.dossiers.get(name=nom_dossier)
  if not dossier:
    raise Exception(f"Dossier '{nom_dossier}' introuvable.")

  lignes = app_tables.participations.search(dossier=dossier)
  for ligne in lignes:
    ligne.delete()

  return "Participations supprimées avec succès."

import pandas as pd
import io
import anvil.server
from anvil.tables import app_tables

@anvil.server.callable
def import_test_participations(nom_dossier, fichier_excel):
  dossier = app_tables.folders.get(name=nom_dossier)
  if not dossier:
    raise Exception(f"Dossier '{nom_dossier}' introuvable.")

  # Lecture du fichier Excel, en précisant le moteur openpyxl
  df = pd.read_excel(
    io.BytesIO(fichier_excel.get_bytes()), 
    header=None, 
    skiprows=1, 
    engine="openpyxl"  # ✅ important
  )

  for _, row in df.iterrows():
    app_tables.participations.add_row(
      folder=dossier,
      societe=row[0],
      actionnaire=row[1],
      type=row[2],
      nb_parts=row[3],
      total_parts_societe=row[4],
      pourcentage=row[5],
      groupe=row[6],
      sous_groupe=row[7]
    )

  return "Import Excel terminé avec succès."
