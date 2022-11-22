import requests
from dotenv import dotenv_values


def get_data() -> list[dict]:

    config = dotenv_values(".env")
    
    url = 'https://trouverunlogement.lescrous.fr/api/fr/search/27'

    headers = {
        "accept": "application/ld+json, application/json",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": "SimpleSAMLSessionID=7cf93d422831c329e57766caeb86ec57; HAPROXYID=app4; PHPSESSID="+ config["CROUS_TOKEN"] + "; qpid=cb78nvjfm5tsme57c3cg",
        "Referer": "https://trouverunlogement.lescrous.fr/tools/residual/26/search",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    body= "{\"precision\":6,\"need_aggregation\":true,\"page\":1,\"pageSize\":1000,\"sector\":null,\"idTool\":26,\"occupationModes\":[],\"equipment\":[],\"price\":{\"min\":0,\"max\":null},\"location\":[{\"lon\":-5.4534,\"lat\":51.2683},{\"lon\":9.8678,\"lat\":41.2632}]}"

    reponse = requests.post(url, headers=headers, data=body)
    data = reponse.json()

    accom_list = data['results']['items']

    if len(accom_list) == 0:
        return None

    return accom_list
