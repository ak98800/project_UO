# ✅ ServerModule.py
import anvil.server
import pandas as pd
from anvil.tables import app_tables
from datetime import datetime


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
def get_participations_pour_societe(folder_id, nom_societe):
  folder = app_tables.folders.get_by_id(folder_id)
  if not folder:
    raise Exception("Dossier introuvable.")

  lignes = app_tables.participations.search(folder=folder, societe=nom_societe)
  resultats = []
  for ligne in lignes:
    resultats.append({
      "id": ligne.get_id(),  # ✅ Ajout de l'ID
      "actionnaire": ligne["actionnaire"],
      "type_actionnaire": ligne["type_actionnaire"],
      "pourcentage": ligne["pourcentage"],
      "nb_parts": ligne["nb_parts"]
    })

  return resultats


@anvil.server.callable
def enregistrer_infos_societe(folder_id, nom_societe, total_parts, groupe, sous_groupe):
  from datetime import datetime

  folder = app_tables.folders.get_by_id(folder_id)
  if not folder:
    raise Exception("Dossier introuvable.")

  lignes = app_tables.participations.search(folder=folder, societe=nom_societe)
  if not lignes:
    raise Exception("Aucune ligne de participation pour cette société.")

  for ligne in lignes:
    ligne["total_parts_societe"] = int(total_parts) if total_parts else None
    ligne["groupe"] = groupe
    ligne["sous_groupe"] = sous_groupe
    if not ligne.get("created_at"):
      ligne["created_at"] = datetime.now()

@anvil.server.callable
def ajouter_actionnaire(folder_id, societe, actionnaire, type_actionnaire, pourcentage, nb_parts):
  from datetime import datetime

  folder = app_tables.folders.get_by_id(folder_id)
  if not folder:
    raise Exception("Dossier introuvable.")

  if not societe or not actionnaire:
    raise Exception("Société et actionnaire requis.")

  app_tables.participations.add_row(
    folder=folder,
    societe=societe,
    actionnaire=actionnaire,
    type_actionnaire=type_actionnaire,
    pourcentage=float(pourcentage) if pourcentage else None,
    nb_parts=int(nb_parts) if nb_parts else None,
    created_at=datetime.now()
  )

  return "Actionnaire ajouté"


@anvil.server.callable
def get_infos_societe(folder_id, nom_societe):
  folder = app_tables.folders.get_by_id(folder_id)
  if not folder:
    raise Exception("Dossier introuvable.")

  lignes = app_tables.participations.search(folder=folder, societe=nom_societe)
  if not lignes:
    return {}

  # On prend la première ligne comme source des infos d'en-tête
  ligne = lignes[0]
  return {
    "groupe": ligne["groupe"] if "groupe" in ligne else "",
    "sous_groupe": ligne["sous_groupe"] if "sous_groupe" in ligne else "",
    "total_parts": ligne["total_parts_societe"] if "total_parts_societe" in ligne else ""
  }


@anvil.server.callable
def ajouter_participation_actionnaire(folder_id, societe, actionnaire, type_actionnaire, nb_parts, pourcentage, calcul_auto):
  
  folder = app_tables.folders.get_by_id(folder_id)
  if not folder:
    raise Exception("Dossier introuvable.")

  # Convertir proprement
  nb_parts = float(nb_parts) if nb_parts not in ("", None) else None
  pourcentage = float(pourcentage) if pourcentage not in ("", None) else None

  # Récupération du total_parts_societe
  lignes = app_tables.participations.search(folder=folder, societe=societe)
  total_parts = None
  for ligne in lignes:
    if ligne["total_parts_societe"]:
      total_parts = ligne["total_parts_societe"]
      break

  # 🧠 Logique de calcul / validation
  if calcul_auto:
    if nb_parts is None or total_parts is None:
      raise Exception("Impossible de calculer automatiquement le pourcentage. Vérifiez les parts et le total.")
    pourcentage = round((nb_parts / total_parts) * 100, 2)
  else:
    if pourcentage is None:
      raise Exception("Veuillez saisir un pourcentage ou activer le calcul automatique.")

  # ✅ Enregistrement
  app_tables.participations.add_row(
    folder=folder,
    societe=societe,
    actionnaire=actionnaire,
    type_actionnaire=type_actionnaire,
    nb_parts=nb_parts,
    total_parts_societe=total_parts,
    pourcentage=pourcentage,
    created_at=datetime.now()
  )

  return "OK"


@anvil.server.callable
def supprimer_participation(row_id):
  ligne = app_tables.participations.get_by_id(row_id)
  if ligne:
    ligne.delete()
  else:
    raise Exception("Participation introuvable.")
