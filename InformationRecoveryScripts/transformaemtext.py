import pandas as pd
import os
import re

movies = pd.read_csv("../documents/movies.csv")
tags = pd.read_csv("../documents/tags.csv")

output_dir = "../documents/filmes_com_tags"
os.makedirs(output_dir, exist_ok=True)

movie_dict = dict(zip(movies["movieId"], movies["title"]))

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', " ", filename)

tag_groups = tags.groupby("movieId")["tag"].apply(lambda x: " ".join(x.dropna().astype(str)))

for movie_id, tag_str in tag_groups.items():
    if movie_id in movie_dict:
        movie_name = movie_dict[movie_id]
        safe_movie_name = sanitize_filename(movie_name) 
        file_name = os.path.join(output_dir, f"{safe_movie_name}.txt")
        
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(tag_str)

print("Arquivos de tags criados com sucesso!")