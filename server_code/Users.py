import anvil.email
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import stripe
from datetime import datetime

stripe.api_key = anvil.secrets.get_secret('stripe_secret_api_key')

# ✅ Créer une organisation + profil lié à l'utilisateur (admin)
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

# ✅ Lire le profil du user
@anvil.server.callable
def get_profil(user):
  return app_tables.profiles.get(user=user)

# ✅ Mettre à jour nom + fonction
@anvil.server.callable
def update_profil(user, name, fonction):
  profil = app_tables.profiles.get(user=user)
  if profil:
    profil["name"] = name
    profil["fonction"] = fonction

# ✅ Admin : mettre à jour le nom de l'organisation
@anvil.server.callable
def update_organisation_name(orga_row, new_name):
  if orga_row:
    orga_row["name"] = new_name

# ✅ Exemple simple de fonction protégée
@anvil.server.callable(require_user=True)
def calculate_percentage_of(number, total_number):
  return (int(number) / int(total_number)) * 100

# ✅ Supprimer un user (profil, orga, Stripe, compte)
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

# ✅ Modifier l’email Stripe (si présent)
@anvil.server.callable(require_user=True)
def change_email(email):
  user = anvil.users.get_user()
  try:
    stripe.Customer.modify(user["stripe_id"], email=email)
    user["email"] = email
  except Exception as e:
    print("Erreur Stripe :", e)
  return user

# ✅ Inviter un utilisateur dans une organisation
@anvil.server.callable
def inviter_utilisateur(email, organisation):
  existing_user = app_tables.users.get(email=email)

  if existing_user:
    profil = app_tables.profiles.get(user=existing_user)
    if profil:
      return "Cet utilisateur est déjà membre."
    else:
      app_tables.profiles.add_row(user=existing_user, organisation=organisation, is_admin=False)
      anvil.users.send_password_reset_email(email)
      return "Utilisateur existant invité."
  else:
    new_user = anvil.users.signup_with_email(email, "")
    app_tables.profiles.add_row(user=new_user, organisation=organisation, is_admin=False)
    anvil.users.send_password_reset_email(email)
    return "Nouvel utilisateur invité."

# ✅ Liste des membres d'une organisation
@anvil.server.callable
def lister_utilisateurs_organisation(organisation):
  return app_tables.profiles.search(organisation=organisation)
