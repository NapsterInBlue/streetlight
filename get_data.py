import requests
from bs4 import BeautifulSoup
import pandas as pd

from mapping import build_setlist_dict, all_clean


def crawl_top_show_page(url):
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')

    shows = soup.find_all('div', {'col-xs-12 setlistPreview vevent'})

    dates = []
    songs = []

    for show in shows:
        date = show.find('span', {'class': 'value-title'}).get('title')
        dates.append(date)
        
        url = get_show_url(show)
        setlist = crawl_show_page(url)
        songs.append(setlist)

    return dates, songs


def crawl_show_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    try:
        song_items = soup.find('ol').find_all('li')
    except:
        return []

    setlist = []
    for song_item in song_items:
        if len(song_item.text.split('\n')) > 1:
            if song_item.text.split('\n')[2] != '':
                setlist.append(song_item.text.split('\n')[2])

            else:
                continue

    return setlist


def get_show_url(show_soup):
    BASE = 'https://www.setlist.fm/'

    show_url = show_soup.find('a').get('href')[3:]

    return BASE + show_url


def process_data(all_dates, all_setlists):
    flat_list = [item for sublist in all_setlists for item in sublist]
    setlists = [build_setlist_dict(setlist) for setlist in all_setlists]

    df = pd.DataFrame.from_dict(setlists)
    df['dates'] = all_dates

    df = df[all_clean]

    return df


def load_data():
    df = pd.read_csv('cleaned_data.csv')

    df.index = df['dates']
    df.index = pd.to_datetime(df.index)

    df = df.sort_index()

    del df['dates']

    return df


if __name__ == '__main__':
    URL = r'https://www.setlist.fm/setlists/streetlight-manifesto-6bd68a52.html?page='
    
    all_dates = []
    all_setlists = []

    for i in range(1, 39):
        dates, setlists = crawl_top_show_page(URL+str(i))

        for date, setlist in zip(dates, setlists):
            if len(setlists) != 0:
                all_dates.append(date)
                all_setlists.append(setlist)

    df = process_data(all_dates, all_setlists)
    df.to_csv('cleaned_data.csv', index=False)