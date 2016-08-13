#
# Player - play songs and voice commands
#
import time
import os
import subprocess

class Player:

    def __init__(self, brainz=None, verbose=False):
        self.verbose = verbose
        self.brainz = brainz
        self.started = False
        self.current_song = -1
        self.current_song_played = 0
        self.current_song_length = 0
        self.song_count = 2
        self.songs = ["song1.mp3","song2.mp3"]
        self.songnames = ["Maybe perches have extremely bad music taste. Titanic by Frederic. ","Or maybe fish like classical. Playing Fur Elise."]
        self.song_lengths = [166,166]

    def __print(self, str):
        if self.verbose:
            print ( str)

    def start(self):
        self.started = True

    def stop(self):
        pass

    def tick(self,interval):
        self.current_song_played += interval
        if self.current_song_played > self.current_song_length:
            self.change_song()
        pass

    # Change song.
    # Test sequence is:
    #  - One song length of silence
    #  - Then play the two songs
    # If the songs are off -> dont play anything

    def change_song(self):
        self.__print("Play song")
        if self.brainz.play_music == False:
            self.current_song = -1
            self.current_song_length = 5
            self.current_song_played = 0
            return
        self.current_song += 1
        self.current_song_played = 0

        if self.song_count <= self.current_song:
            self.current_song = -1
            self.current_song_length = self.song_lengths[0]
            self.brainz.web_connection.send_message("Stopped music for a while. Maybe fishes prefer silence.")
        else:
            self.current_song_length = self.song_lengths[self.current_song]
            self.play(self.songs[self.current_song])
            self.brainz.web_connection.send_message( self.songnames[self.current_song])

    def play(self,mp3file):
        self.__print("Play file:" + mp3file)
        FNULL = open(os.devnull, 'w')
# Play music - removed the mp3 files from project ..
#        subprocess.Popen(["omxplayer","--vol","-600",mp3file],stdout=FNULL, stderr=subprocess.STDOUT)

    def talk(self,message):
        if not self.started:
            return
        self.steps = 0
        self.__print("Talking:" + message)
        FNULL = open(os.devnull, 'w')
        subprocess.Popen(["espeak","-s","130","-p","20","-g","2","-k20",message ],stdout=FNULL, stderr=subprocess.STDOUT)
