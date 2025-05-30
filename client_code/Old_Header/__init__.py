from ._anvil_designer import Old_HeaderTemplate
from anvil import *
import anvil.users

class Old_Header(Old_HeaderTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    user = anvil.users.get_user()

    # 🖼️ Image du logo
    logo = Image(source="https://anvil.works/img/logo-square.png", width=40)

    # 👋 Label de bienvenue
    welcome = Label(text=f"Bienvenue, {user['email']}" if user else "Bienvenue !")
    welcome.align = "right"

    # 📐 On aligne à gauche et à droite dans le FlowPanel
    self.header_content.clear()
    self.header_content.add_component(logo)
    self.header_content.add_component(welcome, full_width=True)

