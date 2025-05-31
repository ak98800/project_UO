import anvil
import anvil.email
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import stripe
import random
import string
from datetime import datetime

stripe.api_key = anvil.secrets.get_secret('stripe_secret_api_key')

@anvil.server.callable
def enregistrer_profil(user, name, organisation_name, fonction):
  orga = app_tables.organisations.add_row(
    name=organisation_name,
    created_by=user,
    created_at=datetime.now()
  )
  app_tables.profiles.add_row(
    user=user,
    name=name,
    fonction=fonction,
    organisation=orga,
    is_admin=True
  )

@anvil.server.callable
def get_profil(user):
  profil = app_tables.profiles.get(user=user)
  if not profil:
    return None

  organisation = profil["organisation"]
  return {
    "profil_id": profil.get_id(),  # ✅ plus clair et sûr
    "name": profil["name"],
    "fonction": profil["fonction"],
    "organisation": organisation,
    "organisation_id": organisation.get_id() if organisation else None,
    "is_admin": profil["is_admin"],
    "user": user
  }



@anvil.server.callable
def update_profil(user, name, fonction):
  profil = app_tables.profiles.get(user=user)
  if profil:
    profil["name"] = name
    profil["fonction"] = fonction

@anvil.server.callable
def update_organisation_name(orga_row, new_name):
  if orga_row:
    orga_row["name"] = new_name

@anvil.server.callable(require_user=True)
def calculate_percentage_of(number, total_number):
  return (int(number) / int(total_number)) * 100

@anvil.server.callable(require_user=True)
def delete_user():
  user = anvil.users.get_user()
  profil = app_tables.profiles.get(user=user)
  orga = profil["organisation"] if profil else None
  is_admin = profil["is_admin"] if profil else False

  if profil:
    profil.delete()

  if orga and is_admin:
    autres = app_tables.profiles.search(organisation=orga)
    if len(autres) == 0:
      orga.delete()

  if "stripe_id" in user and user["stripe_id"]:
    try:
      stripe.Customer.delete(user["stripe_id"])
    except Exception as e:
      print("Stripe delete error:", e)

  user.delete()

@anvil.server.callable(require_user=True)
def change_email(email):
  user = anvil.users.get_user()
  try:
    stripe.Customer.modify(user["stripe_id"], email=email)
    user["email"] = email
  except Exception as e:
    print("Erreur Stripe :", e)
  return user

@anvil.server.callable
def inviter_utilisateur(email, name, organisation):
  current_user = anvil.users.get_user()
  if not current_user:
    raise Exception("Utilisateur non connecté.")
  if email == current_user["email"]:
    raise Exception("Vous ne pouvez pas vous inviter vous-même.")

  # ✅ Vérifie si l'utilisateur existe
  existing_user = app_tables.users.get(email=email)

  if existing_user:
    # ✅ Si déjà membre
    if app_tables.profiles.get(user=existing_user):
      return "Cet utilisateur est déjà membre."

    # ✅ Sinon : ajouter le profil et envoyer reset
    app_tables.profiles.add_row(
      user=existing_user,
      name=name,
      organisation=organisation,
      is_admin=False
    )
    anvil.users.send_password_reset_email(email)
    return "Utilisateur existant invité."

  else:
    # ✅ Crée le user via signup (envoi email automatique de confirmation)
    temp_password = "AnvilTemp123"
    new_user = anvil.users.signup_with_email(email, temp_password)

    # ✅ Corrige le nom exact : confirmed_email
    new_user["confirmed_email"] = True  # ⚠️ exactement ce nom-là
    new_user.update()

    # ✅ Crée le profil
    app_tables.profiles.add_row(
      user=new_user,
      name=name,
      organisation=organisation,
      is_admin=False
    )

    # ✅ Envoie uniquement l’email de reset
    anvil.users.send_password_reset_email(email)

    return "Nouvel utilisateur invité."




@anvil.server.callable
def lister_utilisateurs_organisation(organisation):
  return app_tables.profiles.search(organisation=organisation)

@anvil.server.callable(require_user=True)
def supprimer_utilisateur(profil):
  connected = anvil.users.get_user()
  if profil and profil["user"] != connected:
    user_to_delete = profil["user"]
    profil.delete()
    if user_to_delete:
      user_to_delete.delete()
    return "Utilisateur supprimé."
  else:
    raise Exception("Vous ne pouvez pas vous supprimer vous-même.")


@anvil.server.callable
def get_membres_dossier(folder_id):
  print(f"✅ Fonction appelée avec folder_id = {folder_id}")

  folder = app_tables.folders.get_by_id(folder_id)
  if not folder:
    raise Exception(f"Dossier introuvable pour ID : {folder_id}")

  membres = app_tables.folder_members.search(folder=folder)
  result = []

  for m in membres:
    user = m["user"]
    if not user:
      continue

    email = user["email"]
    user_id = user.get_id()

    # 🔍 Recherche du profil via ID du user
    profil = None
    for p in app_tables.profiles.search():
      if p["user"] and p["user"].get_id() == user_id:
        profil = p
        break

        # 💬 Debug clair
    if profil:
      print(f"✅ Profil trouvé pour {email} → profil_id = {profil.get_id()}, name = {profil['name']}")
    else:
      print(f"❌ Aucun profil trouvé pour {email} (user_id = {user_id})")

    name = profil["name"] if profil and profil["name"] else "(nom inconnu)"


    result.append({
      "id": m.get_id(),
      "user_id": user_id,
      "email": email,
      "name": name,
      "is_admin": m["is_admin"],
      "folder_id": folder.get_id()
    })

  print("📤 Membres retournés :", result)
  return result




















@anvil.server.callable
def partager_dossier_par_email(email, folder_id):
  user = app_tables.users.get(email=email)
  if not user:
    raise Exception("Utilisateur non trouvé")

  folder = app_tables.folders.get_by_id(folder_id)
  if not app_tables.folder_members.get(folder=folder, user=user):
    app_tables.folder_members.add_row(folder=folder, user=user, is_admin=False)
    return "Utilisateur ajouté avec succès"
  else:
    return "Cet utilisateur a déjà accès à ce dossier."

@anvil.server.callable
def retirer_utilisateur_dossier(folder_id, user_id):
  folder = app_tables.folders.get_by_id(folder_id)
  user = app_tables.users.get_by_id(user_id)

  if not folder or not user:
    raise Exception("Dossier ou utilisateur introuvable.")

  membre = app_tables.folder_members.get(folder=folder, user=user)

  if not membre:
    raise Exception("Le membre n'existe pas dans ce dossier.")

  if membre["is_admin"]:
    raise Exception("Impossible de supprimer un administrateur du dossier.")

  membre.delete()


