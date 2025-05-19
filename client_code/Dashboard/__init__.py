from ._anvil_designer import DashboardTemplate
from anvil import *
import anvil.server
import anvil.users

class Dashboard(DashboardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user = anvil.users.get_user()

    # Appliquer le rôle CSS à la sidebar
    self.sidebar_panel.role = "sidebar"

    # Message de bienvenue
    if self.user:
      email = self.user["email"]
      self.label_welcome.text = f"Bienvenue, {email} !"
    else:
      self.label_welcome.text = "Bienvenue !"

  def calculate_button_click(self, **event_args):
    """Exemple d'action possible sur le dashboard"""
    try:
      number1 = float(self.number_1_textbox.text)
      number2 = float(self.number_2_textbox.text)

      if number2 == 0:
        Notification("Le dénominateur ne peut pas être zéro.", style="danger").show()
        return

      result = anvil.server.call("calculate_percentage_of", number1, number2)
      self.answer_text.text = f"{number1} est {result}% de {number2}"
      self.answer_text.visible = True

    except Exception as e:
      Notification(f"Erreur : {str(e)}", style="danger").show()




