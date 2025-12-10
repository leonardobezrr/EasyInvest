from bs4 import BeautifulSoup
import requests
import csv

pageToScrape = requests.get('https://quotes.toscrape.com/')
soup = BeautifulSoup(pageToScrape.text, 'html.parser')

quotes = soup.find_all('span', attrs={'class': 'text'})
authors = soup.find_all('small', attrs={'class': 'author'})

file = open('quotes.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(file)
writer.writerow(['Quote', 'Author'])

for quote,author in zip(quotes,authors):
    print(quote.text, '-\n', author.text)
    writer.writerow([quote.text, author.text])
file.close()