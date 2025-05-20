from ._anvil_designer import UserItemTemplate
from anvil import *

class UserItem(UserItemTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    profil = self.item

    self.nom_label.text = profil["name"]
    self.fonction_label.text = profil["fonction"]
    self.email_label.text = profil["user"]["email"]

