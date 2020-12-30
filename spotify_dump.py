#!/usr/bin/python3

import argparse
import os
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials

def loadConfig(aConfigFile):
    with open(aConfigFile, 'r') as read_from:
        for line in read_from:
            key, value = line.split(maxsplit=1)
            os.environ[key] = value.rstrip()

def addArguments(aArgumentParser):
    aArgumentParser.add_argument('-c', '--config', nargs='?', default='config.cfg', help='Specifies a new config file')
    aArgumentParser.add_argument('-o', '--output', nargs='?', default='out.log', help='Specifies the output file')
    aArgumentParser.add_argument('-a', '--artists', action='store_true', help='Retrieves all artists from playlist')

if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    addArguments(argument_parser)
    arguments = argument_parser.parse_args()
    loadConfig(arguments.config)

    client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    playlist = client.user_playlist_tracks(os.environ['SPOTIPY_USER'], os.environ['SPOTIPY_PLAYLIST'])
    tracks = playlist['items']
    while playlist['next']:
        playlist = client.next(playlist)
        tracks.extend(playlist['items'])
    with open(arguments.output, 'w+') as f:
        for track in tracks:
            if arguments.artists:
                for artist in track['track']['artists']:
                    f.write(artist['name'] + '\n')

