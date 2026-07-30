import pandas as pd

""" 
    Merge the IMDb Title Basics and Title Ratings into a single CSV file. The data are pre-filtered to reduce the number of movies that need to be queried through the TMDB API.
"""

df_title = pd.read_csv("../data/raw/title.basics.tsv", sep="\t", encoding="utf-8")
df_rating = pd.read_csv("../data/raw/title.ratings.tsv", sep="\t", encoding="utf-8")

df_final = df_title.merge(right=df_rating, how="left", on=["tconst"])

filter = (
          (df_final["titleType"] == "movie") & 
          (df_final["startYear"] <= "2026") &  
          (df_final["startYear"] >= "2022") & 
          (df_final["startYear"] != r"\N") & 
          (~df_final["isAdult"] ) &
          (df_final["numVotes"] > 1500)
)

""" 
    Remove unnecessary columns
"""

columns = df_final.columns.drop(["endYear", "isAdult", "titleType", "originalTitle"])
df_final = df_final[filter][columns].sort_values(by="numVotes")

df_final.to_csv("../data/raw/films_imdb.csv", encoding="utf-8", index=False)


