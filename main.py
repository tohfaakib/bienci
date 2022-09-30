import csv
import requests


def save_csv(url, raw_json):
    global save_csv_call_counter
    fields = [url, raw_json]
    header = ['url', 'raw_json']
    with open('bienci_output_dep1.csv', 'a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if save_csv_call_counter == 0:
            writer.writerow(header)
        writer.writerow(fields)
    save_csv_call_counter += 1


def parse(page, frm, z_id, min_price=None, max_price=None):
    global ccc

    if min_price is None:
        price_filter = f'"maxPrice":{max_price},'
    elif max_price is None:
        price_filter = f'"minPrice":{min_price},'
    else:
        price_filter = f'"minPrice":{min_price},"maxPrice":{max_price},'

    params = {
        'filters': '{"size":24,"from":' + str(
            frm) + ',"showAllModels":false,"filterType":"buy","propertyType":["house"],' + price_filter + '"page":' + str(
            page) + ',"sortBy":"relevance","sortOrder":"desc","onTheMarket":[true],"zoneIdsByTypes":{"zoneIds":["' + str(
            z_id) + '"]}}',
        'extensionType': 'extendedIfNoResult',
        'leadingCount': '2',
        'access_token': 'wKjv6GwoeehtTD5u+lRNdREYXSwMnRyrityqbkxrwGg=:628dde8a0d860600b6571f33',
        'id': '628dde8a0d860600b6571f33',
    }

    response = requests.get('https://www.bienici.com/realEstateAds.json', params=params)

    data = response.json()["realEstateAds"]
    data_check = []
    for d in data:
        if d["id"] not in done:
            url = 'https://www.bienici.com/annonce/a/a/a/a/' + d["id"]
            print(url)
            save_csv(url, d)
            done.append(d["id"])
            with open("done.txt", "a") as faaa:
                faaa.write(str(d["id"]) + "\n")
            data_check.append(d["id"])
    if len(data_check) == 0:
        return "Break"


def zone_id(n):
    params = {
        'q': str(n),
    }

    response = requests.get('https://res.bienici.com/place.json', params=params)
    return response.json()["zoneIds"][0]


if __name__ == '__main__':
    save_csv_call_counter = 0
    with open('done.txt', 'r') as f:
        done = f.read().splitlines()

    done = [x.strip() for x in done]

    for i in range(1, 99, 1):
        # url = f"https://www.bienici.com/recherche/achat/{i}/maisonvilla"
        print("zone_n:", i)
        if i == 96:
            continue
        z_id = zone_id(i)
        print("zone_id:", z_id)
        for j in range(1, 7):
            if j == 1:
                ma = j * 100000
                mi = None
            elif j == 6:
                ma = None
                mi = (j - 1) * 100000
            else:
                ma = j * 100000
                mi = (j - 1) * 100000

            print("min_price:", mi)
            print("max_price:", ma)
            for page in range(1, 101):
                print('page:', page)
                frm = 24 * (page - 1)
                print('frm:', frm)
                sig = parse(page=page, frm=frm, z_id=z_id, min_price=mi, max_price=ma)
                if sig == "Break":
                    break

        # break
