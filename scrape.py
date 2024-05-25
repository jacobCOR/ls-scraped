import itertools
from random import random
from time import sleep, time

from bs4 import BeautifulSoup
import requests
import sqlite3


def linkshell_scrape(name: str):
    conn = sqlite3.connect('linkshell.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS linkshells (
        id TEXT PRIMARY KEY,
        name TEXT,
        server TEXT
    )
    ''')
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS characters (
        id TEXT,
        name TEXT,
        linkshell TEXT,
        server TEXT,
        date INTEGER,
        PRIMARY KEY (id, linkshell),
        FOREIGN KEY (linkshell) REFERENCES linkshells(id) ON DELETE CASCADE
    )
    ''')
    alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ':', "!", "?"]
    # Generate singletons
    singletons = [(x,) for x in alphabets]  # Convert to tuples to match the format of pairs and triplets
    
    # Generate pairs
    pairs = list(itertools.combinations(alphabets, 2))
    
    # Generate triplets
    triplets = list(itertools.combinations(alphabets, 3))

# Combine all into one variable
    all_combinations = singletons + pairs + triplets
    for keyword in all_combinations:
        keyword = ''.join(keyword)
        n = 0
        while n <= 20:
            url = f"https://na.finalfantasyxiv.com/lodestone/crossworld_linkshell/?q={keyword}&dcname={name.capitalize()}&character_count=&page={n}&order="
            page = requests.get(url)
            if page.status_code != 200:
                break
            soup = BeautifulSoup(page.content, 'html.parser')
            linkshells = soup.find_all('div', class_='entry')
            for linkshell in linkshells:
                try:
                    ls_id = linkshell.find('a', class_="entry__link--line").get('href').split('/')[-2]
                except:
                    break
                linkshell_server = linkshell.find('p').text
                # insert into db id is pk text
                # check if exists first
                c.execute("SELECT 1 FROM linkshells WHERE id = ?", (ls_id,))
                exists = c.fetchone() is not None
                if exists:
                    continue
                c.execute("INSERT OR IGNORE INTO linkshells (id, name, server) VALUES (?, ?, ?)", (ls_id, linkshell_server, name))
                print(f"ID: {ls_id} Server: {linkshell_server}")
                
                # get characters
                characters = requests.get(f"https://na.finalfantasyxiv.com/lodestone/crossworld_linkshell/{ls_id}/")
                character_soup = BeautifulSoup(characters.content, 'html.parser')
                character_list = character_soup.find_all('div', class_='entry')
                for character in character_list:
                    try:
                        char_id = character.find('a', class_="entry__link").get('href').split('/')[-2]
                        print(char_id)
                    except:
                        continue
                    char_name = character.find('p').text
                    c.execute("INSERT INTO characters (id, name, linkshell, date, server) VALUES (?, ?, ?, ?, ?)", (char_id, char_name, ls_id, int(time()), name))
                    print(f"ID: {char_id} Name: {char_name}")
            n += 1

        # random between 0.8 and 1.2 seconds
            sleep((0.8 + 0.4 * random()))
            conn.commit()
    conn.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    linkshell_scrape('aether')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
