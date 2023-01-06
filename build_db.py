import sqlite3
import cedict
import pinyin

conn = sqlite3.connect("dictionary.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS dictionary")
cur.execute("""CREATE TABLE dictionary(
  simplified CHAR(32),
  traditional CHAR(32),
  english CHAR(256),
  pinyin CHAR(128),
  hsk INT
)""")

dic = cedict.read()
cur.executemany(
  "INSERT INTO dictionary (simplified, traditional, english, pinyin, hsk) VALUES (?, ?, ?, ?, ?)",
  map(lambda w: (w.simplified, w.traditional, w.english, w.pinyin, None), dic)
)

conn.commit()
