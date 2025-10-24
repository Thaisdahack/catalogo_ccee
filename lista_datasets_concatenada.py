import pandas as pd

import pandas as pd

# Caminhos dos arquivos 
lista1 = pd.read_csv("lista_datasets.csv")
lista2 = pd.read_csv("lista_perda_horario.csv")

# Concatenar as duas listas 
lista_total = pd.concat([lista1, lista2], ignore_index=True)

# Remover duplicados 
lista_total = lista_total.drop_duplicates()

# Salvar o resultado em um novo CSV
lista_total.to_csv("lista_datasets_completa.csv", index=False, encoding="utf-8")

print("✅ Listas concatenadas e salvas em 'lista_concatenada.csv' com sucesso!")
