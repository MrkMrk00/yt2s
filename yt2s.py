#!/usr/bin/env python

import os.path
import json
from selenium import webdriver
import yt2s.scraper as scraper

def browser_open():
    driver = webdriver.Firefox()
    driver.get('https://www.youtube.com/')

    return driver

def main():
    input_opt: str = ''

    if not os.path.exists('./out'):
        os.mkdir('./out');

    webdriver = browser_open()
    while input_opt != ':q':
        input_opt = input('> ')

        if input_opt == 'playlist':
            playlist = scraper.scrape_playlist(webdriver)
            file_name = f'./out/{playlist.name}_{playlist.id}.json'
            print(f'{file_name=}')

            with open(file_name, 'w') as playlist_file:
                json.dump(
                    playlist,
                    playlist_file,
                    default=lambda o: o.__dict__,
                    indent=4,
                )
                playlist_file.write('\n')


if __name__ == '__main__':
    main()

