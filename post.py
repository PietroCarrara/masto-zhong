import sqlite3
import pinyin

from mastodon import Mastodon
from dotenv import load_dotenv
from os import getenv
from cedict import Word

def fetch_random_word(cur, min_hsk = 1, max_hsk = 6):
  cur.execute("""
    SELECT
      simplified,
      traditional,
      pinyin,
      english,
      hsk
    FROM
      dictionary
    WHERE
      id IN (SELECT id FROM dictionary WHERE hsk >= ? AND hsk <= ? ORDER BY RANDOM() LIMIT 1)
  """, (min_hsk, max_hsk))
  simplified, traditional, pinyin, english, hsk = cur.fetchone()

  w = Word()
  w.simplified = simplified
  w.traditional = traditional
  w.pinyin = pinyin
  w.english = english

  return w, hsk

def fetch(cur, simpl):
    cur.execute("""
      SELECT
        simplified,
        traditional,
        pinyin,
        english
      FROM
        dictionary
      WHERE
        simplified = ?
    """, (simpl))

    res = []
    for tuple in cur.fetchall():
      simplified, traditional, pinyin, english = tuple

      w = Word()
      w.simplified = simplified
      w.traditional = traditional
      w.pinyin = pinyin
      w.english = english

      res.append(w)

    return res

load_dotenv()

acc = getenv("ACCESS")
cid = getenv("CLIENTID")
csc = getenv("CLIENTSECRET")
api = getenv("API")

min_hsk = int(getenv("MINHSK"))
max_hsk = int(getenv("MAXHSK"))

mastodon = Mastodon(api_base_url = api, access_token = acc)

conn = sqlite3.connect("dictionary.db")
cur = conn.cursor()

word, hsk = fetch_random_word(cur, min_hsk, max_hsk)

character = word.simplified if word.simplified == word.traditional else f"{word.simplified}/{word.traditional}"
mastodon.status_post(
  f"{pinyin.decode(word.pinyin)}\n{word.english}\nhttps://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=0&wdqb={word.simplified}",
  spoiler_text = f"HSK{hsk}: {character}"
)