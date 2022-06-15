import pandas as pd
import json

#変換したいJSONファイルを読み込む
fp = "beidol_2021-12-13T01-28-35.json"
df = pd.read_json(fp,orient="records",lines=True)
dfd = df.drop_duplicates(subset='tel')
dfd.to_csv(f'{fp.split(".")[0]}.csv', encoding='utf-8')