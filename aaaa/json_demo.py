import json

with open('states.json') as f:
# 위 코드는 f = open('test.txt') 와 비슷하지만 with문은 블록내에서만 파일을 열고닫습니다
    data = json.load(f)

for state in data['states']:
    del state['area_codes']

with open('new_states.json', 'w') as f:
    json.dump(data, f, indent=2)