import requests
from bs4 import BeautifulSoup


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


if __name__ == '__main__':
    URL = r'https://www.setlist.fm/setlists/streetlight-manifesto-6bd68a52.html?page='
    
    all_dates = []
    all_setlists = []

    for i in range(1, 34):
        dates, setlists = crawl_top_show_page(URL+str(i))

        for date, setlist in zip(dates, setlists):
            if len(setlists) != 0:
                all_dates.append(date)
                all_setlists.append(setlist)
