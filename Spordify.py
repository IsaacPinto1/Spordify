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

def scrape(songs, attribute): # 0: key, 1: bpm

    # take in songs as [name artist, ID]

    d = {
        "A Major": 0,
        "A Minor": 1,
        "A# Major": 2,
        "A# Minor": 3,
        "B♭ Major": 4,
        "B♭ Minor": 5,
        "B Major": 6,
        "B Minor": 7,
        "C Major": 8,
        "C Minor": 9,
        "C# Major": 10,
        "C# Minor": 11,
        "D♭ Major": 12,
        "D♭ Minor": 13,
        "D Major": 14,
        "D Minor": 15,
        "D# Major": 16,
        "D# Minor": 17,
        "E♭ Major": 18,
        "E♭ Minor": 19,
        "E Major": 20,
        "E Minor": 21,
        "F Major": 22,
        "F Minor": 23,
        "F# Major": 24,
        "F# Minor": 25,
        "G♭ Major": 26,
        "G♭ Minor": 27,
        "G Major": 28,
        "G Minor": 29,
        "G# Major": 30,
        "G# Minor": 31,
        "A♭ Major": 32,
        "A♭ Minor": 33
    }


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get("https://tunebat.com/")

    for song in songs:
        search = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CLASS_NAME, "ant-input-lg")) #find search bar

        search.send_keys(song[0]) #input song name

        search.send_keys(Keys.ENTER)

        WebDriverWait(driver, timeout=10).until(EC.none_of(lambda d: d.find_element(By.CLASS_NAME,"anticon-loading-3-quarters"))) # wait until page loads

        page_source = driver.page_source

        soup = BeautifulSoup(page_source,features="html.parser")
        key = soup.find_all("div", class_="k43JJ")
        key = key[attribute] # 0: key, 1: bpm
        key = key.find("p",class_="lAjUd")
        if attribute == 1:
            song[0] = key.text
        else:
            song[0] = d[key.text]
    return songs
    
def nameSort():
    order = []
    for track in results['items']: # for every track in the playlist
        order.append([track['track']['name'] + " " + track['track']['artists'][0]['name'],
        track['track']['uri']])
    # Generate array as [name artist, ID]
    
    order.sort()
    order = [element[1] for element in order]
    reorder(order)

def artistSort():
    order = []
    for track in results['items']: # for every track in the playlist
        order.append([track['track']['artists'][0]['name'],
        track['track']['uri']])
    # Generate array as [artist, ID]
    
    order.sort()
    order = [element[1] for element in order]
    reorder(order)

def albumSort():
    order = []
    for track in results['items']: # for every track in the playlist
        order.append([track['track']['album']['name'],
        track['track']['uri']])
    # Generate array as [album, ID]

    order.sort()
    order = [element[1] for element in order]
    reorder(order)

def durationSort():
    order = []
    for track in results['items']: # for every track in the playlist
        order.append([track['track']['duration_ms'],
        track['track']['uri']])
    # Generate array as [duration, ID]
    
    order.sort()
    order = [element[1] for element in order]
    reorder(order)

def bpmSort():
    order = []
    for track in results['items']: # for every track in the playlist
        order.append([track['track']['name'] + " " + track['track']['artists'][0]['name'],
        track['track']['uri']])
    # Generate array as [name artist, ID]
    
    order = scrape(order, 1)
    order = sorted(order, key=lambda x: int(x[0]))
    print(order)
    order = [element[1] for element in order]
    reorder(order)

def keySort():
    order = []
    for track in results['items']: # for every track in the playlist
        order.append([track['track']['name'] + " " + track['track']['artists'][0]['name'],
        track['track']['uri']])
    # Generate array as [name artist, ID]
    
    order = scrape(order, 0)
    order.sort()
    order = [element[1] for element in order]
    reorder(order)

##### Get user choice:
questions = [
  inquirer.List('sort',
                message="Choose a sorting option",
                choices=['Name', 'Artist', 'Album', 'Duration', 'BPM', 'Key'],
            ),
]
answers = inquirer.prompt(questions)
choice = answers['sort']

if choice == 'Name':
    nameSort()
elif choice == 'Artist':
    artistSort()
elif choice == 'Album':
    albumSort()
elif choice == 'Duration':
    durationSort()
elif choice == 'BPM':
    bpmSort()
elif choice == 'Key':
    keySort()
