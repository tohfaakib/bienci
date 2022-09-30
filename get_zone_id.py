import requests


def zone_id(n):
    params = {
        'q': str(n),
    }

    response = requests.get('https://res.bienici.com/place.json', params=params)
    # print(response.text)
    return response.json()["zoneIds"][0]


for i in range(1, 99, 1):
    if i == 96:
        continue
    zone = zone_id(i)
    with open('zone_id.txt', 'a') as f:
        f.write(f'{i}: {zone}\n')
    print(zone)

# print(zone_id(1))
