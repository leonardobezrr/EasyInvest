from bs4 import BeautifulSoup
import requests

import requests
from bs4 import BeautifulSoup

# User-Agent Autêntico para Windows 10/11 + Chrome Recente
# Nota: 'Windows NT 10.0' serve tanto para Win10 quanto Win11
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://www.google.com/',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"'
}


pageToScrape = 'https://investidor10.com.br/acoes/raiz4/'
response = requests.get(pageToScrape, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

print(f"Status Code: {response.status_code}")

cards = soup.find_all('div', attrs={'class': 'communication-card'})
print(f"Encontrei {len(cards)} comunicados. Listando títulos:\n")

for communicate in cards:
    print(communicate.text)