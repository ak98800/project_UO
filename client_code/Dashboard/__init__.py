from ._anvil_designer import DashboardTemplate
from anvil import *
import anvil.server
import anvil.users
# Assure-toi d’importer tes autres pages :
# from ..DossiersPage import DossiersPage
# from ..FichiersPage import FichiersPage
# etc.

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

  # 👇 Ces méthodes doivent être à l'intérieur de la classe
  def link_dossiers_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(DossiersPage())

  def link_fichiers_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(FichiersPage())

  def link_visualisation_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(VisualisationPage())

  def link_ajouter_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(NouvelleAnalysePage())

  def link_utilisateurs_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(GestionUtilisateursPage())

  def link_profil_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(MonProfilPage())

  def link_logout_click(self, **event_args):
    anvil.users.logout()
    open_form("MainPage")

  def icon_button_menu_1_click(self, **event_args):
    pass
