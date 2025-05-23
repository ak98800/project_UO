import anvil.email
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
from datetime import date


@anvil.server.callable
def creer_dossier(nom_dossier, profil):
  user = anvil.users.get_user()
  if not user or not profil:
    raise Exception("Utilisateur non connecté ou profil manquant.")

  folder = app_tables.folders.add_row(
    name=nom_dossier,
    created_by=user,
    created_at=datetime.now(),
    organisation=profil["organisation"]
  )

  app_tables.folder_members.add_row(
    folder=folder,
    user=user,
    is_admin=True,
    added_at=datetime.now()
  )

  return folder

@anvil.server.callable
def get_dossiers(organisation):
  user = anvil.users.get_user()
  if not user:
    raise Exception("Utilisateur non connecté.")

  membres = app_tables.folder_members.search(user=user)
  dossiers = []

  for membre in membres:
    folder = membre['folder']
    if folder and folder['organisation'] == organisation:
      nb_users = len(app_tables.folder_members.search(folder=folder))
      dossiers.append({
        "id": folder.get_id(),
        "nom": folder["name"],
        "created_by": folder["created_by"],
        "organisation": folder["organisation"],  # ✅ ajoute ceci
        "created_at": folder["created_at"],
        "nb_users": nb_users
      })

  return dossiers

@anvil.server.callable
def supprimer_dossier(folder_id):
  user = anvil.users.get_user()
  folder = app_tables.folders.get_by_id(folder_id)

  if not folder:
    raise Exception("Dossier introuvable.")
  if folder["created_by"] != user:
    raise Exception("Vous n'êtes pas autorisé à supprimer ce dossier.")

  # Supprimer les participations liées
  for ligne in app_tables.participations.search(folder=folder):
    ligne.delete()

  # Supprimer les membres liés
  for membre in app_tables.folder_members.search(folder=folder):
    membre.delete()

  # Supprimer le dossier
  folder.delete()

@anvil.server.callable
def partager_dossier_avec_utilisateur(profil, folder_id):
  user = anvil.users.get_user()
  folder = app_tables.folders.get_by_id(folder_id)

  if not folder or folder["created_by"] != user:
    raise Exception("Non autorisé à partager ce dossier.")

  user_to_add = profil["user"]

  if app_tables.folder_members.get(folder=folder, user=user_to_add):
    return "Cet utilisateur a déjà accès à ce dossier."

  app_tables.folder_members.add_row(
    folder=folder,
    user=user_to_add,
    is_admin=False,
    added_at=datetime.now()

  )

  return "Accès accordé avec succès."

