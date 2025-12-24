import anvil.email
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


@anvil.server.callable
def get_be_paths(dossier_name, societe_cible, max_paths=50000):
  """
  Retourne tous les chemins montants depuis societe_cible vers les ultimes.
  Chaque chemin contient:
    - ultime
    - type ("PP"/"PM")
    - path: ["ULTIME", "...", "CIBLE"]
    - pct_path: % d'intérêt de l'ultime dans la cible (produit des %)
    - calc: "x% × y% × z%"
    - depth: nb de liens
  """

  dossier_row = app_tables.folders.get(name=dossier_name)
  if not dossier_row:
    raise Exception(f"Dossier '{dossier_name}' introuvable.")

  rows = app_tables.participations.search(folder=dossier_row)

  # parents_of[child] = [(parent, pct, type_parent)]
  parents_of = {}
  type_map = {}  # type_map[entity] = "PP"/"PM"

  for r in rows:
    parent = r["actionnaire"]
    child = r["societe"]
    pct = float(r["pourcentage"] or 0.0)
    t = r["type_actionnaire"] or "PM"
    if not parent or not child:
      continue
    parents_of.setdefault(child, []).append((parent, pct, t))
    type_map[parent] = t

  def is_ultime(name):
    # Ultime si PP OU si personne ne le détient dans ce dossier
    if type_map.get(name) == "PP":
      return True
    return name not in parents_of  # pas de parent enregistré

  paths = []
  count = 0

  # On remonte: current = entité actuelle, factor = % cumulé (en %),
  # chain_nodes = [CIBLE, ..., current], chain_pcts = [pct1, pct2, ...] dans le sens montée
  def dfs_up(current, factor, chain_nodes, chain_pcts, visited):
    nonlocal count
    if count >= max_paths:
      return

    # Si current est ultime => on enregistre un chemin
    if is_ultime(current):
      # current est l’ultime. chain_nodes est [CIBLE, ..., ULTIME]
      path_nodes = list(reversed(chain_nodes))  # [ULTIME, ..., CIBLE]
      pcts = list(reversed(chain_pcts))         # % dans le sens [ULTIME -> ... -> CIBLE]
      calc = " × ".join([f"{p:g}%" for p in pcts]) if pcts else ""
      paths.append({
        "ultime": current,
        "type": type_map.get(current, "PM"),
        "path": path_nodes,
        "pct_path": factor,
        "calc": calc,
        "depth": len(pcts)
      })
      return

    # Sinon, on explore ses parents
    for parent, pct, t_parent in parents_of.get(current, []):
      if parent in visited:
        continue  # évite boucles
      count += 1
      new_factor = factor * (pct / 100.0)
      dfs_up(
        parent,
        new_factor,
        chain_nodes + [parent],
        chain_pcts + [pct],
        visited | {parent}
      )

  # Start: la cible vaut 100%
  dfs_up(societe_cible, 100.0, [societe_cible], [], {societe_cible})

  # tri: ultimes puis % chemin décroissant
  paths.sort(key=lambda x: (x["ultime"], -float(x["pct_path"] or 0.0)))
  return paths
