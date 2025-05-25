# ✅ ServerModule.py
import anvil.server
import pandas as pd
from anvil.tables import app_tables

@anvil.server.callable
def get_synthese_participations(dossier_id):
  from collections import defaultdict
  from anvil.tables import app_tables

  dossier = app_tables.folders.get_by_id(dossier_id)
  if not dossier:
    raise Exception("Dossier introuvable.")

  participations = app_tables.participations.search(folder=dossier)

  # Regrouper les participations par société
  regroupement = defaultdict(list)
  for ligne in participations:
    regroupement[ligne["societe"]].append(ligne)

  resultat = []
  for societe, lignes in regroupement.items():
    total = sum(l["pourcentage"] or 0 for l in lignes)
    statut = "✅"
    if total < 100:
      statut = "⚠️"
    elif total > 100:
      statut = "❌"

    resultat.append({
      "societe": societe,
      "nb_actionnaires": len(lignes),
      "total_pourcentage": round(total, 2),
      "statut": statut
    })

  return sorted(resultat, key=lambda x: x["societe"])



@anvil.server.callable
def verifier_societe_unique(dossier_id, nom_societe):
  dossier = app_tables.folders.get_by_id(dossier_id)
  if not dossier:
    raise Exception("Dossier introuvable.")

  existante = app_tables.participations.search(folder=dossier, societe=nom_societe)
  if len(list(existante)) > 0:
    raise Exception("Cette société existe déjà dans le dossier.")

  return nom_societe




@anvil.server.callable
def verifier_societe_unique(folder_id, nom_societe):
  folder = app_tables.folders.get_by_id(folder_id)
  if not folder:
    raise Exception("Dossier introuvable.")

  # Vérifie si la société existe déjà dans ce dossier
  existe = app_tables.participations.search(folder=folder, societe=nom_societe)
  if any(existe):
    raise Exception(f"La société '{nom_societe}' existe déjà dans ce dossier.")

  return nom_societe
