from bs4 import BeautifulSoup
import requests
import csv

# Use consistent variable names
column_names = ['Entry Number', 'Name', 'Year', 'Game Price', 'Platform', 'Total Votes']

with open('main.csv', 'a', encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(column_names)

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }

    site = requests.get('https://steam250.com/top250', headers=headers).text
    soup = BeautifulSoup(site, 'lxml')
    games = soup.find_all('div', class_="appline")
    c = 1

    for game in games:
        name = game.find('span', class_="title").text.split('. ')[1:]
        name = "{}".format(*name)
        game_date = game.find('span', class_="date").text if game.find('span', class_="date") else ""
        game_price = game.find('span', class_="price").text if game.find('span', class_="price") else "უასოა"
        game_content = game.find('a', class_="g2 tag").text if game.find('a', class_="g2 tag") else "N/A"
        game_platform = game.find('span', class_="platform")
        mac = game.find('a', class_="mac")
        win = game.find('a', class_="win")
        deck = game.find('a', class_="deck")

        x = [c, name, game_date, game_price,game_content]

        if mac and win and deck:
            x.append("Mac, Win, Deck")
        elif mac and win:
            x.append("Mac, Win")
        elif mac and deck:
            x.append("Mac, Deck")
        elif win and deck:
            x.append("Win, Deck")
        elif mac:
            x.append("Mac")
        elif win:
            x.append("Win")
        elif deck:
            x.append("Deck")
        else:
            x.append("არ არის არცერთზე")

        c += 1
        csvwriter.writerow(x)

print(f"Done writing {c} entries to the CSV file!")
