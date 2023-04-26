import numpy as np
import pandas as pd
import os
import sys
import multiprocessing as mp
from dotenv import load_dotenv
from lyricsgenius import Genius
from tqdm.auto import tqdm

load_dotenv()
genius_token = os.getenv("GENIUS_ACCESS_TOKEN")
genius = Genius(genius_token)
# load pickle file
artists_dict = pd.read_pickle("../dict_featuresALL-modified.pickle")
df = pd.read_csv("../nodes.csv")
print(df)
artist_list = df.iloc[:, 1].to_numpy()

files = os.listdir()
done_list = artist_list
files = [f.split(".")[0] for f in files if f.endswith(".json")]
remaining = np.setdiff1d(done_list, files)
print(f"There are {len(remaining)} artist left")


def get_artist(artist):
    try:
        genius_artist = genius.search_artist(
            artist, max_songs=3, sort="popularity", allow_name_change=True
        )
        genius_artist.save_lyrics(f"{artist}", verbose=False, overwrite=True)

    except Exception as e:
        print(e)


with mp.Pool(3) as pool:
    results = list(tqdm(pool.imap(get_artist, remaining), total=len(remaining)))
