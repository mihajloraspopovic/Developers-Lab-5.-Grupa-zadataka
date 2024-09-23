import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('Urban Air Quality and Health Impact Dataset.csv')

print("Prvih nekoliko redova dataset-a:")
print(df.head())

print("\nKolone u datasetu:")
print(df.columns)

print("\nIzaberi kolonu koja sadrzi brojcane vrijednosti:")
numeric_columns = df.select_dtypes(include=[np.number]).columns
for idx, col in enumerate(numeric_columns, 1):
    print(f"{idx}. {col}")
selected_index = int(input("\nUnesi broj kolone: ")) - 1
selected_column = numeric_columns[selected_index]

print(f"\nIzabrana kolona: {selected_column}")

min_value = df[selected_column].min()
max_value = df[selected_column].max()
print(f"\nNajmanja vrijednost u koloni {selected_column}: {min_value}")
print(f"Najveća vrijednost u koloni {selected_column}: {max_value}")

mean_value = df[selected_column].mean()
print(f"\nProsječna vrijednost u koloni {selected_column}: {mean_value}")

percentage_diff = ((max_value - mean_value) / mean_value) * 100
print(f"\nProcentualna razlika između prosječne i najveće vrijednosti: {percentage_diff:.2f}%")

df[selected_column] = (df[selected_column] - min_value) / (max_value - min_value)

df.to_csv('Urban_Air_Quality_Normalized.csv', index=False)
print(f"\nNormalizovana kolona je sačuvana u novom fajlu: Urban_Air_Quality_Normalized.csv")

correlation_matrix = df.corr()
correlations = correlation_matrix.unstack().sort_values()

max_positive_corr = correlations[(correlations != 1.0) & (correlations > 0)].idxmax()
max_negative_corr = correlations[(correlations < 0)].idxmin()

print(f"\nNajveća pozitivna korelacija je između kolona: {max_positive_corr}, vrijednost: {correlations[max_positive_corr]:.2f}")
print(f"Najveća negativna korelacija je između kolona: {max_negative_corr}, vrijednost: {correlations[max_negative_corr]:.2f}")

print("\nStandardna devijacija za svaku kolonu:")
std_devs = df.std()
print(std_devs)

for column in numeric_columns:
    plt.figure(figsize=(8, 6))
    plt.hist(df[column], bins=20, color='blue', alpha=0.7)
    plt.title(f'Raspodjela vrijednosti za kolonu: {column}')
    plt.xlabel(column)
    plt.ylabel('Frekvencija')
    plt.grid(True)
    plt.show()