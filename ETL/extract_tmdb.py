import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

"""
    Loads the access_token from the .env file and includes it in the request header to authenticate GET requests to the TMDB API. It then reads the list of films extracted from IMDb and retrieves their corresponding tconst values (IMDb's unique title identifiers), which are used to match the IMDb data with the TMDB records.
"""

load_dotenv()

df = pd.read_csv("../data/raw/films_imdb.csv", encoding="utf-8")

idIMDB = df["tconst"].tolist()

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv("access_token")}"
}

"""
    Each film requires two API requests. The first retrieves its TMDB ID using the IMDb tconst identifier. The second uses the TMDB ID to fetch the film's detailed information. If an error occurs at any stage, the saveError function records the film's identifier along with the step at which the error occurred, allowing the issue to be analyzed and handled later.
"""

def saveerror(id, errortype):
    with open ("data/tmdberrors.txt", mode="a", encoding="utf-8") as op:
        op.write(f"{id} {errortype} \n")

"""
    Since the target dataset contains approximately 5,200 films, processing them sequentially would take a considerable amount of time. To improve performance, the concurrent.futures library is used to execute multiple API requests simultaneously through a pool of threads. The as_completed function processes each completed request as soon as it finishes, allowing the results to be written to the JSON file incrementally without the risk of overwriting data. This approach reduces the total execution time from approximately two hours to around thirty minutes.
"""

def getjson(i):

    findUrl = f"https://api.themoviedb.org/3/find/{i}?external_source=imdb_id"

    response = requests.get(findUrl, headers=headers)

    if response.status_code == 200:
        if response.json()["movie_results"]:
            idTMDB = response.json()["movie_results"][0]["id"]
        else:
            return "error_find"
    else:
        return "error_find"
    
    detailsUrl = f"https://api.themoviedb.org/3/movie/{idTMDB}"

    response = requests.get(detailsUrl, headers=headers)

    if response.status_code == 200:

        return response.json()

    else:
        return "error_details"


with ThreadPoolExecutor(max_workers=30) as executor:
    
    futures = {
            executor.submit(getjson, tconst): tconst 
            for tconst in idIMDB
        }
    
    for future in as_completed(futures):
        
        tconst = futures[future]

        data = future.result()
        
        if data == "error_find":
            saveerror(tconst, "find")

        elif data == "error_details":
            saveerror(tconst, "details")
            
        elif data:  
            with open ("data/tmdbdata.jsonl", mode="a", encoding="utf-8") as file:
                strdata = json.dumps(data, ensure_ascii=False)
                file.write(strdata + "\n")
