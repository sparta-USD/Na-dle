import json
from pprint import pprint
with open('music_data.json', 'r') as f:
    test = json.load(f)
pprint(test)

new_list = []
for t in test:
    new_data = {"model":"musics.music"}
    new_data["fields"] = {}
    new_data["fields"]["id"] = t["music_id"]+1
    new_data["fields"]["title"] = t["title"]
    new_data["fields"]["album"] = t["album"]
    new_data["fields"]["artist"] = t["artist"]
    new_data["fields"]["image"] = t["image"]
    new_data["fields"]["track_id"] = t["track_id"]
    new_list.append(new_data)
    
pprint(new_list)

with open('music_data_for_db.json', 'w', encoding='UTF-8') as f:
    # dump(데이터 json객체, 파일, ensure_ascii: 아스키 코드로 변경 여부, indent: 들여쓰기 몇개할건지)
    json.dump(new_list, f, ensure_ascii=False, indent=2)

# 터미널에 아래 코드를 입력하면 db에 저장됨
# python manage.py loaddata music_data_for_db.json