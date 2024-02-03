import urllib.parse
from dataclasses import dataclass, field
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

@dataclass
class Song:
    title: str
    artist: str | None
    url: str


@dataclass
class Playlist:
    name: str
    id: str
    songs: list[Song] = field(default_factory=list)


def _yoink_songs(driver: WebDriver):
    song_elements = driver.find_elements(By.CSS_SELECTOR, '#contents ytd-playlist-video-renderer')
    for song_element in song_elements:
        title = song_element.find_element(By.CSS_SELECTOR, '#video-title').text
        artist = song_element.find_element(By.CSS_SELECTOR, 'yt-formatted-string.ytd-channel-name').text or ''
        if '- Topic' in artist:
            artist = artist.replace(' - Topic', '')

        url = song_element.find_element(By.CSS_SELECTOR, '#video-title').get_attribute('href') or ''

        yield Song(
            title=urllib.parse.unquote(title),
            artist=urllib.parse.unquote(artist),
            url=urllib.parse.unquote(url)
        )


def scrape_playlist(driver: WebDriver) -> Playlist:
    parsed_url = urllib.parse.urlparse(driver.current_url)
    query = urllib.parse.parse_qs(parsed_url.query)

    id = query['list'][0]
    name = driver.title.split('-')[0].strip()

    return Playlist(name=name, id=id, songs=list(_yoink_songs(driver)))

