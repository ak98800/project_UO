import anvil.server
from anvil.tables import app_tables
import anvil.tables.query as q


@anvil.server.callable
def get_dossiers_disponibles():
  user = anvil.users.get_user()
  if not user:
    raise Exception("Utilisateur non connecté.")

  # Récupérer tous les dossiers liés à l'utilisateur via folder_members
  liens = app_tables.folder_members.search(user=user)

  # Extraire les noms uniques des dossiers autorisés
  noms_dossiers = set()
  for lien in liens:
    folder = lien['folder']
    if folder:
      noms_dossiers.add(folder['name'])

  return sorted(noms_dossiers)

@anvil.server.callable
def get_relations_dossier(nom_dossier):
  # Filtrer les participations liées au dossier sélectionné
  rows = app_tables.participations.search()
  relations = []
  for row in rows:
    dossier = row['folder']
    if dossier and dossier['name'] == nom_dossier:
      actionnaire = row['actionnaire']
      societe = row['societe']
      pourcentage = row['pourcentage'] or 0
      if actionnaire and societe:
        relations.append((actionnaire, societe, pourcentage))
  return relations

@anvil.server.callable
def get_relations_dossier_typed(nom_dossier):
  rows = app_tables.participations.search()
  results = []
  for row in rows:
    folder = row['folder']
    if folder and folder['name'] == nom_dossier:
      actionnaire = row['actionnaire']
      societe = row['societe']
      pourcentage = row['pourcentage'] or 0
      type_actionnaire = row['type_actionnaire'] or "PM"
      if actionnaire and societe:
        results.append((actionnaire, societe, pourcentage, type_actionnaire))
  return results


@anvil.server.callable
def get_liste_societes_du_dossier(nom_dossier):
  user = anvil.users.get_user()

  # 1. Chercher le dossier par nom
  dossier = app_tables.folders.get(name=nom_dossier)
  if not dossier:
    raise Exception("Dossier introuvable.")

    # 2. Vérifier que ce user est bien membre via folder_members
  lien = app_tables.folder_members.get(folder=dossier, user=user)
  if not lien:
    raise Exception("Accès non autorisé à ce dossier.")

    # 3. Extraire les sociétés liées à ce dossier
  lignes = app_tables.participations.search(folder=dossier)
  noms = list({ligne['societe'] for ligne in lignes if ligne['societe']})

  return [{"name": nom, "dossier": dossier} for nom in noms]



@anvil.server.callable
def get_relations_descendantes(dossier_name, point_depart):
  print(f"\n--- get_relations_descendantes ---")
  print(f"Dossier demandé : {dossier_name}")
  print(f"Société de départ : {point_depart}")

  # 1. Récupérer la ligne du dossier
  dossier_row = app_tables.folders.get(name=dossier_name)
  if not dossier_row:
    raise Exception(f"Dossier '{dossier_name}' introuvable.")

  # 2. Récupérer les participations du dossier
  rows = app_tables.participations.search(folder=dossier_row)
  print(f"Nombre de participations trouvées : {len(rows)}")

  # 3. Construire le graphe actionnaire → société
  graphe = {}
  type_map = {}

  for row in rows:
    actionnaire = row['actionnaire']
    societe = row['societe']
    pourcentage = row['pourcentage'] or 0
    type_act = row['type_actionnaire'] or "PM"

    if not actionnaire or not societe:
      continue

    if actionnaire not in graphe:
      graphe[actionnaire] = []

    graphe[actionnaire].append((societe, pourcentage, type_act))
    type_map[actionnaire] = type_act

  print(f"Nombre de nœuds (actionnaires) dans le graphe : {len(graphe)}")
  if point_depart not in graphe:
    print(f"⚠️ Aucun lien descendant trouvé pour : {point_depart}")

  # 4. DFS depuis point_depart
  visited = set()
  result = []

  def dfs(current):
    if current in graphe:
      for societe, pourcentage, type_act in graphe[current]:
        if (current, societe) not in visited:
          visited.add((current, societe))
          result.append((current, societe, pourcentage, type_act))
          dfs(societe)

  dfs(point_depart)

  print(f"Relations descendantes trouvées : {len(result)}")
  for r in result:
    print(r)

  return result



@anvil.server.callable
def get_relations_montantes(dossier_name, point_depart, max_edges=2000):
  print(f"\n--- get_relations_montantes ---")
  print(f"Dossier demandé : {dossier_name}")
  print(f"Société de départ : {point_depart}")

  dossier_row = app_tables.folders.get(name=dossier_name)
  if not dossier_row:
    raise Exception(f"Dossier '{dossier_name}' introuvable.")

  rows = app_tables.participations.search(folder=dossier_row)
  print(f"Nombre de participations trouvées : {len(rows)}")

  # Graphe SOCIETE -> [(ACTIONNAIRE, %, type_act)]
  parents_of = {}
  for row in rows:
    actionnaire = row['actionnaire']
    societe = row['societe']
    pourcentage = row['pourcentage'] or 0
    type_act = row['type_actionnaire'] or "PM"
    if not actionnaire or not societe:
      continue
    parents_of.setdefault(societe, []).append((actionnaire, pourcentage, type_act))

  print(f"Nombre de nœuds (sociétés) dans le graphe : {len(parents_of)}")
  if point_depart not in parents_of:
    print(f"⚠️ Aucun lien montant direct trouvé pour : {point_depart}")

  # visited_edges évite doublons (actionnaire->societe)
  visited_edges = set()

  # visited_nodes évite boucles infinies (A possède B, B possède A, etc.)
  visited_nodes = set()

  result = []

  def dfs(current_societe):
    if current_societe in visited_nodes:
      return
    visited_nodes.add(current_societe)

    for actionnaire, pourcentage, type_act in parents_of.get(current_societe, []):
      edge_key = (actionnaire, current_societe)
      if edge_key in visited_edges:
        continue

      visited_edges.add(edge_key)

      # On garde le sens "détenteur -> détenu" (cohérent avec descendante)
      result.append((actionnaire, current_societe, pourcentage, type_act))

      if len(result) >= max_edges:
        return

      # IMPORTANT : on remonte aussi les parents de l'actionnaire
      # (car un actionnaire peut lui-même être une société dans la table)
      dfs(actionnaire)

  dfs(point_depart)

  print(f"Relations montantes trouvées : {len(result)}")
  return result



@anvil.server.callable
def get_ultimes_interets(dossier_name, societe_cible, max_paths=50000):
  """
  Retourne une liste de tuples:
    (ultime, societe_cible, pct_total, type_ultime)
  où pct_total est la somme des % d'intérêt de l'ultime dans la cible.
  """

  dossier_row = app_tables.folders.get(name=dossier_name)
  if not dossier_row:
    raise Exception(f"Dossier '{dossier_name}' introuvable.")

  rows = app_tables.participations.search(folder=dossier_row)

  # parents_of[SOCIETE] = [(ACTIONNAIRE, pct, type_actionnaire)]
  parents_of = {}
  type_map = {}  # type_map[ACTIONNAIRE] = "PP" / "PM"
  for r in rows:
    actionnaire = r["actionnaire"]
    societe = r["societe"]
    pct = float(r["pourcentage"] or 0)
    type_act = r["type_actionnaire"] or "PM"
    if not actionnaire or not societe:
      continue
    parents_of.setdefault(societe, []).append((actionnaire, pct, type_act))
    type_map[actionnaire] = type_act

  # Accumulateur des intérêts ultimes
  totals = {}  # totals[ultime] = pct_total (en %)
  paths_count = 0

  def is_ultime(name):
    # Ultime si PP, OU si personne ne le détient dans le dossier (pas de parent enregistré)
    if type_map.get(name) == "PP":
      return True
    return name not in parents_of

  def dfs(current, factor, path_nodes):
    """
    current: entité dont on cherche les parents
    factor: % cumulé depuis l'ultime jusqu'à la cible (exprimé en %)
    path_nodes: set pour éviter cycles
    """
    nonlocal paths_count
    if paths_count > max_paths:
      return

    # Si current est ultime -> on accumule
    if is_ultime(current):
      totals[current] = totals.get(current, 0.0) + factor
      return

    # Sinon on remonte ses parents
    for parent, pct, _type_act in parents_of.get(current, []):
      if parent in path_nodes:
        continue  # évite boucles
      paths_count += 1
      # Exemple: parent détient pct% de current, et current pèse factor% de la cible
      new_factor = factor * (pct / 100.0)
      dfs(parent, new_factor, path_nodes | {parent})

  # point de départ : la cible vaut 100%
  dfs(societe_cible, 100.0, {societe_cible})

  # Sortie sous forme edges vers la cible
  result = []
  for ultime, pct_total in totals.items():
    # type ultime si connu, sinon PM
    t = type_map.get(ultime, "PM")
    result.append((ultime, societe_cible, pct_total, t))

  # tri décroissant %
  result.sort(key=lambda x: x[2], reverse=True)
  return result
