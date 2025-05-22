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
  return app_tables.profiles.get(user=user)

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

  existing_user = app_tables.users.get(email=email)

  if existing_user:
    profil = app_tables.profiles.get(user=existing_user)
    if profil:
      return "Cet utilisateur est déjà membre."
    else:
      app_tables.profiles.add_row(
        user=existing_user,
        name=name,
        organisation=organisation,
        is_admin=False
      )
      return "Utilisateur existant invité."
  else:
    temp_password = "AnvilTemp123"
    new_user = anvil.users.signup_with_email(email, temp_password)

    app_tables.profiles.add_row(
      user=new_user,
      name=name,
      organisation=organisation,
      is_admin=False
    )
    return "Nouvel utilisateur invité. Il doit confirmer son email."

@anvil.server.callable(require_user=True)
def envoyer_reset_si_invite():
  user = anvil.users.get_user()
  profil = app_tables.profiles.get(user=user)
  if not profil:
    raise Exception("Profil introuvable.")
  if not user["email_confirmed"]:
    raise Exception("Veuillez d'abord confirmer votre email.")

  anvil.users.send_password_reset_email(user["email"])
  return "Lien de réinitialisation envoyé."

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
