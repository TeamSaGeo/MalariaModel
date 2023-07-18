import pandas as pd
import sys, os

filepath = sys.argv[1]
if os.path.exists(filepath):
  df = pd.read_csv(filepath, sep=";")
  result = df.melt(id_vars=["CodeCommune","type_donnees","numero_annee"], var_name="Semaine", value_name="valeur")
  result_sorted = result.sort_values(by=["numero_annee", "Semaine"],ascending=True)
  new_path = os.path.splitext(filepath)[0] + "_pivoted.csv"
  result_sorted.to_csv(new_path, sep=";", index=False)
  print("Pivot du données terminé avec succès!\nRésultat stocké dans le fichier" + new_path)
else:
  print("Argument chemin du fichier de données météo source absent! Utliser la commande suivante:\npython .\script_pivot_sem_meteo.py [chemin du fichier])")
