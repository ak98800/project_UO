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

# Créer une organisation + profil lié à l'utilisateur
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

# Lire le profil du user
@anvil.server.callable
def get_profil(user):
  return app_tables.profiles.get(user=user)

# Mettre à jour le nom + fonction
@anvil.server.callable
def update_profil(user, name, fonction):
  profil = app_tables.profiles.get(user=user)
  if profil:
    profil["name"] = name
    profil["fonction"] = fonction

# Si admin : modifier le nom de l’organisation
@anvil.server.callable
def update_organisation_name(orga_row, new_name):
  if orga_row:
    orga_row["name"] = new_name

# Stripe - changement d'email
@anvil.server.callable(require_user=True)
def change_email(email):
  user = anvil.users.get_user()
  try:
    customer = stripe.Customer.modify(user["stripe_id"], email=email)
    user["email"] = email
  except stripe.error.StripeError as e:
    print("Stripe API error:", e)
  except Exception as e:
    print("Error:", e)
  return user

# Stripe - suppression utilisateur
@anvil.server.callable(require_user=True)
def delete_user():
  user = anvil.users.get_user()
  if user["stripe_id"]:
    try:
      stripe.Customer.delete(user["stripe_id"])
    except Exception as e:
      print("Stripe delete error:", e)
  user.delete()
