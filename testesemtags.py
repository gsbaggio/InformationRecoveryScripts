import pandas as pd

filmes = pd.read_csv("../documents/movies.csv", encoding="utf-8")
tags = pd.read_csv("../documents/tags.csv", encoding="utf-8")

filmes_com_tags = set(tags["movieId"].unique())

filmes_sem_tags = filmes[~filmes["movieId"].isin(filmes_com_tags)]

print(f"Total de filmes sem tags: {len(filmes_sem_tags)}")
print(filmes_sem_tags.head())

filmes_sem_tags.to_csv("../documents/filmes_sem_tags.csv", index=False, encoding="utf-8")