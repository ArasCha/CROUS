import requests
import json

url = 'https://trouverunlogement.lescrous.fr/api/fr/search/26'


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
    "cookie": "SimpleSAMLSessionID=7cf93d422831c329e57766caeb86ec57; HAPROXYID=app4; PHPSESSID=darhvv9g5aqe5goddnsuugekbd; qpid=cb78nvjfm5tsme57c3cg",
    "Referer": "https://trouverunlogement.lescrous.fr/tools/residual/26/search",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

body = '{\"precision\":6,\"need_aggregation\":true,\"page\":1,\"pageSize\":24,\"sector\":null,\"idTool\":26,\"occupationModes\":[],\"equipment\":[],\"price\":{\"min\":0,\"max\":null},\"location\":[{\"lon\":-1.6418,\"lat\":47.2959},{\"lon\":-1.4788,\"lat\":47.1806}]}'


reponse = requests.post(url, headers=headers, data=body)

code_json = reponse.json()

resultat = code_json.get('results').get('items')

print(resultat)

# j=0

# for i in resultat:

# 	logement=resultat[j].get('residence').get("label")
# 	print(logement)
# 	j+=1

