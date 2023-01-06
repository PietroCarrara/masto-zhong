import sqlite3
import cedict

conn = sqlite3.connect("dictionary.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS dictionary")
cur.execute("""CREATE TABLE dictionary(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  simplified CHAR(32),
  traditional CHAR(32),
  english CHAR(256),
  pinyin CHAR(128),
  classifier CHAR(64),
  hsk INT
)""")

dic = cedict.read()
cur.executemany(
  "INSERT INTO dictionary (simplified, traditional, english, pinyin, classifier, hsk) VALUES (?, ?, ?, ?, ?, ?)",
  map(lambda w: (w.simplified, w.traditional, w.english, w.pinyin, w.classifier, None), dic)
)

hsk_lists = {
  1: "hsk/HSK-1.csv",
  2: "hsk/HSK-2.csv",
  3: "hsk/HSK-3.csv",
  4: "hsk/HSK-4.csv",
  5: "hsk/HSK-5.csv",
  6: "hsk/HSK-6.csv",
}

for level in hsk_lists:
  with open(hsk_lists[level]) as f:
    for w in f.readlines():
      w = w.strip()

      # Separate structures
      for word in w.split('…'):
        if w == '':
          continue

        cur.execute(
          'UPDATE dictionary SET hsk = ? WHERE simplified = ? AND (hsk IS NULL OR hsk > ?)',
          (level, word, level)
        )


conn.commit()
