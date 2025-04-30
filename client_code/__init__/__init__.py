from .LoginPage import LoginPage

class __init__(__init__Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Rediriger vers LoginPage avec message de confirmation
    LoginPage(confirmed=True)
