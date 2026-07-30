import json
import pandas as pd

"""
    A função tocsv passa transforma o dataframe enviado para csv, evitando repetição de código
"""

def tocsv(df:pd.DataFrame, filename:str):

    df.to_csv(f"../data/processed/{filename}.csv", encoding="utf-8", index=False)


"""
    Each line in tmdbdata.jsonl contains a separate JSON object with the data for a single film. These records are loaded into a list of dictionaries and then converted into a pandas DataFrame.
    This is the primary reason for retrieving data from TMDB: the IMDb datasets do not include box office revenue or production budget information. These financial data are extracted from TMDB and saved in financial.csv, together with their corresponding film IDs, allowing them to be linked with the other datasets during later stages of the analysis.
"""
data = []

with open ("../data/raw/tmdbdata.jsonl", mode="r", encoding="utf-8") as open_file:

    for line in open_file:
        info = json.loads(line)
        data.append(
            {
                "tconst" : info["imdb_id"],
                "budget" : info["budget"],
                "boxoffice" : info["revenue"],
                "profit" : info["revenue"] - info["budget"]
            }
        )
    
df_financial = pd.DataFrame(data)


"""
    Films with extremely low budgets or box office revenues are filtered out, as they are either not relevant to the analysis or contain unreliable data (such as a recorded box office revenue of zero). The remaining valid film IDs are then saved and used to filter the subsequent DataFrames.
"""

filter = (df_financial["budget"] > 500) & (df_financial["boxoffice"] > 5000000)

df_financial = df_financial[filter].sort_values(by="boxoffice")

useful_ids = df_financial["tconst"]

tocsv(df_financial, "financial")



"""
    Only the films that passed the previous filtering stage are relevant for the analysis. Therefore, each DataFrame is filtered using the isin() method with the list of valid film IDs.
"""    

df_films = pd.read_csv("../data/raw/films_imdb.csv", encoding="utf-8")

df_films = df_films[df_films["tconst"].isin(useful_ids)]



"""
    The genres column is extracted from the main films DataFrame and stored in a separate DataFrame. Like the financial data, genres are linked to their corresponding films through the film ID, allowing the relationship to be established whenever needed during the analysis.
"""

df_genres = df_films[["tconst","genres"]]

df_genres["genres"] = df_genres["genres"].str.split(",")
df_genres = df_genres.explode("genres")

tocsv(df_genres, "genres")


columns = df_films.columns.drop("genres")
df_films = df_films[columns]

df_films["runtimeMinutes"] = df_films["runtimeMinutes"].astype(int)
df_films["numVotes"] = df_films["numVotes"].astype(int)

df_films = df_films.rename(columns=
            {
                "startYear" : "releaseYear"
            })

tocsv(df_films, "films")


"""
    The crew dataset contains the directors and writers associated with each film. These records are separated into individual DataFrames to optimize the analysis. Since each field is stored as a single comma-separated string, the values are first split using split(","), and the explode() function is then applied to transform each list of directors or writers into separate rows, with each row containing only a single individual.
"""

df_crew = pd.read_csv("../data/raw/title.crew.tsv", encoding="utf-8", sep="\t")

df_crew = df_crew[df_crew["tconst"].isin(useful_ids)]

df_directors = df_crew[["tconst", "directors"]]
df_writers = df_crew[["tconst", "writers"]]

df_directors["directors"] = df_directors["directors"].str.split(",")
df_writers["writers"] = df_writers["writers"].str.split(",")

df_directors = df_directors.explode("directors")
df_writers = df_writers.explode("writers")

df_directors = df_directors.rename(columns=
            {
                "directors" : "nconst"
            })

df_writers = df_writers.rename(columns=
            {
                "writers" : "nconst"
            })

tocsv(df_directors, "directors")
tocsv(df_writers, "writers")

"""
    As with the films filtered using the list of valid IDs, only the records corresponding to the people referenced in df_directors and df_writers are retained. This filtering is performed using the useful_crew list, ensuring that only relevant crew members are saved for the analysis.
"""


useful_crew = pd.concat([df_writers["writers"], df_directors["directors"]])

df_crewdetails = pd.read_csv("../data/raw/name.basics.tsv", encoding="utf-8", sep="\t")

df_crewdetails = df_crewdetails[df_crewdetails["nconst"].isin(useful_crew)]

df_crewdetails = df_crewdetails[["nconst", "primaryName", "birthYear","deathYear"]]

df_crewdetails = df_crewdetails.rename(columns=
            {
                "primaryName" : "crewName"
            })

tocsv(df_crewdetails, "crew")
