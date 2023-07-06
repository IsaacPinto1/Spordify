import spotipy
from spotipy.oauth2 import SpotifyOAuth
import inquirer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random



######## Copy the following into terminal:
#export SPOTIPY_CLIENT_ID=<CLIENT_ID>
#export SPOTIPY_CLIENT_SECRET=<CLIENT_SECRET>
#export SPOTIPY_REDIRECT_URI="<REDIRECT_URI>"

scope = ["user-library-read", "user-library-modify", "playlist-modify-public"]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
PLAYLIST = input("Enter playlist link: ")
results = sp.playlist_tracks(PLAYLIST) # results = playlist details


def reorder(order):
    for i in range(len(order)):
        sp.playlist_remove_all_occurrences_of_items(PLAYLIST, [order[i]]) # delete track from playlist
        sp.playlist_add_items(PLAYLIST, [order[i]]) # append it to the end

def makeArray(choice):
    order = []
    if choice == 'Name' or choice == 'BPM' or choice == 'Key' or choice == 'Randomize':
        for track in results['items']:
            if track['track']['is_local']:
                continue
            order.append([track['track']['name'] + " - " + track['track']['artists'][0]['name'],
            track['track']['uri']])
            # Generate array as [name - artist, ID]


    elif choice == 'Artist':
        for track in results['items']:
            if track['track']['is_local']:
                continue
            order.append([track['track']['artists'][0]['name'],
            track['track']['uri']])
            # Generate array as [artist, ID]


    elif choice == 'Album':
        for track in results['items']:
            if track['track']['is_local']:
                continue
            order.append([track['track']['album']['name'],
            track['track']['uri']])
            # Generate array as [album, ID]


    elif choice == 'Duration':
        for track in results['items']:
            if track['track']['is_local']:
                continue
            order.append([track['track']['duration_ms'],
            track['track']['uri']])
            # Generate array as [duration, ID]


    return order

def report(order, choice): # 0: key, 2: BPM
    for i in range(len(order)):
        if choice == 0:
            print(str(i+1) + ". " + order[i][0] + ": " + order[i][2])
        elif choice == 2:
            print(str(i+1) + ". " + order[i][0] + ": " + order[i][2] + " BPM")

def sort(choice):
    order = makeArray(choice)
    if choice == 'BPM':
        order = scrape(order, 2)
        order = sorted(order, key=lambda x: int(x[2]))
        report(order, 2)
    elif choice == 'Key':
        order = scrape(order, 0)
        order = sorted(order, key=lambda x: x[3])
        report(order, 0)
    elif choice == 'Randomize':
        random.shuffle(order)
    else:
        order.sort()
    order = [element[1] for element in order]
    reorder(order)

def scrape(songs, attribute): # 0: key, 2: bpm

    # take in songs as [name - artist, ID]
    d = {
        "A": 0,
        "A♯/B♭": 1,
        "B": 2,
        "C": 3,
        "C♯/D♭": 4,
        "D": 5,
        "D♯/E♭": 6,
        "E": 7,
        "F": 8,
        "F♯/G♭": 9,
        "G": 10,
        "G♯/A♭": 11
    }

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://songbpm.com/searches/3cad117e-42f0-4b57-b62d-b1c797d46fcf")
    driver.minimize_window()

    def loaded(song):
        page_source = driver.page_source
        soup = BeautifulSoup(page_source,features="html.parser")
        key = soup.find("h1", class_="mb-8")
        return key.text[16:].lower() == song.lower()

    for song in songs:
        search = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.NAME, "query")) #find search bar

        search.clear()
        search.send_keys(song[0]) #input song name

        search.send_keys(Keys.ENTER)

        while True:
            if loaded(song[0]):
                break

        page_source = driver.page_source

        soup = BeautifulSoup(page_source,features="html.parser")
        key = soup.find_all("span", class_="sm:text-3xl")
        key = key[attribute] # 0: key, 2: bpm
        song.append(key.text)
        if attribute == 0:
            song.append(d[key.text])
    return songs # return as [name - artist, ID, BPM] or [name - artist, ID, key, key translation]
    
##### Get user choice:
questions = [
  inquirer.List('sort',
                message="Choose a sorting option",
                choices=['Name', 'Artist', 'Album', 'Duration', 'BPM', 'Key', 'Randomize'],
            ),
]
answers = inquirer.prompt(questions)
choice = answers['sort']
sort(choice)



##### To Do: