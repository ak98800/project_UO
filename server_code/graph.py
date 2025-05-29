# ✅ ServerModule.py
import anvil.server
import pandas as pd
from anvil.tables import app_tables
from datetime import datetime


@anvil.server.callable
def get_graph_data_for_dossier(dossier_id):
  return {
    "nodes": [
      {"id": "A", "label": "Holding"},
      {"id": "B", "label": "Filiale 1"},
      {"id": "C", "label": "Filiale 2"}
    ],
    "edges": [
      {"from": "A", "to": "B"},
      {"from": "A", "to": "C"}
    ]
  }
