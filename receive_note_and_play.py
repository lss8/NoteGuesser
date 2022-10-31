
import time
import pygame as pg

from mingus.midi import midi_file_out
from mingus.containers import Note
from sympy import true

def receive_a_note_to_play(note, repeat=1):
    note_to_play = Note(note , 4)
    midi_file_out.write_Note("note.mid", note_to_play , 45)

    return create_music("note.mid", repeat)

def create_music(file, repeat):
    music_file = file
    repeat_times = repeat

    freq = 44100  
    bitsize = -16   
    channels = 2    
    buffer = 2048   

    pg.mixer.init(freq, bitsize, channels, buffer)
    pg.mixer.music.set_volume(1.0)

    try:
        for i in range(repeat_times):
            play_music(music_file)
            time.sleep(1)
        return (True)
    except KeyboardInterrupt:
        pg.mixer.music.fadeout(1000)
        pg.mixer.music.stop()
        raise SystemExit

def play_music(music_file):
    clock = pg.time.Clock()
    try:
        pg.mixer.music.load(music_file)
    except pg.error:
        return
    pg.mixer.music.play()
    while pg.mixer.music.get_busy():
        clock.tick(30)