from ._anvil_designer import ImportTempDevPageTemplate
from anvil import *
import anvil.server
import anvil.media


class ImportTempDevPage(ImportTempDevPageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def import_button_click(self, **event_args):
    nom_dossier = self.nom_dossier_textbox.text.strip()
    if not nom_dossier:
      Notification("Veuillez saisir un nom de dossier.", style="warning").show()
      return

    if not self.fichier_excel_loader.file:
      Notification("Veuillez charger un fichier Excel.", style="warning").show()
      return

    try:
      result = anvil.server.call("import_test_participations", nom_dossier, self.fichier_excel_loader.file)
      Notification(result, style="success").show()
    except Exception as e:
      Notification(f"Erreur : {e}", style="danger").show()

  def nettoyer_button_click(self, **event_args):
    nom_dossier = self.nom_dossier_textbox.text.strip()
    if not nom_dossier:
      Notification("Veuillez saisir un nom de dossier.", style="warning").show()
      return

    try:
      result = anvil.server.call("supprimer_participations_dossier", nom_dossier)
      Notification(result, style="info").show()
    except Exception as e:
      Notification(f"Erreur : {e}", style="danger").show()


  def export_button_click(self, **event_args):
    nom_dossier = self.nom_dossier_textbox.text.strip()
    if not nom_dossier:
      Notification("Veuillez saisir un nom de dossier.", style="warning").show()
      return

    try:
      fichier_excel = anvil.server.call("exporter_participations_dossier", nom_dossier)
      if fichier_excel:
        download(fichier_excel)
      else:
        Notification("Aucune donnée trouvée pour ce dossier.", style="warning").show()
    except Exception as e:
      Notification(f"Erreur lors de l'export : {e}", style="danger").show()

