import time
import numpy as np
import pyaudio
import random

# freq related constants
FSAMP = 22050       
FRAME_SIZE = 2048   
FRAMES_PER_FFT = 16 
RATE = 44100   
SAMPLE_SIZE = 8

SAMPLES_PER_FFT = FRAME_SIZE*SAMPLE_SIZE
FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT

# notes related constants
NOTES_INTERVAL = 'C C# D D# E F F# G G# A A# B'.split()
MIN_NOTE = 60       # C4
MAX_NOTE = 69       # A4

# freq and note name retrival functions
def freq_to_number(f): return 69 + 12*np.log2(f/440.0)
def number_to_freq(n): return 440 * 2.0**((n-69)/12.0)
def note_name(n): return NOTES_INTERVAL[n % 12]

# fft related functions
def note_to_fftbin(n): return number_to_freq(n)/FREQ_STEP
imin = max(0, int(np.floor(note_to_fftbin(MIN_NOTE-1))))
imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(MAX_NOTE+1))))


class NoteChecker:
    
    # since we're not considering sharp notes
    notes_to_check = 'C D E F G A B'.split()

    # open stream to wait for sound
    def open_audio(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            frames_per_buffer=FRAME_SIZE,
        )
    
    # close stream  
    def close_audio(self):
            self.stream.close()
            self.audio.terminate()
            print("Stop listening now, thanks for playing!")

    # switch wanted note
    def switch_note(self, note):
        self.wanted_note = note
        print(f"Now this note: {note}")
    
    # sort of main function
    def note_checker(self):
        self.open_audio()
        random.shuffle(self.notes_to_check)
        
        # decide wanted note
        for n in self.notes_to_check:
            self.switch_note(n)
            self.note_loop()
        
        self.close_audio()
       
    # loop to test input frequency    
    def note_loop(self):
        num_frames = 0
        last_n = [0] * SAMPLE_SIZE
        buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
        window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))

        while True:
            time.sleep(0.1)
            buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
            buf[-FRAME_SIZE:] = np.fromstring(self.stream.read(FRAME_SIZE), np.int16)

            # run the FFT 
            fft = np.fft.rfft(buf*window)
            freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP

            # save freq
            last_n[num_frames] = int(freq)
            num_frames += 1

            if num_frames == SAMPLE_SIZE:
                num_frames = 0
                this_avg = sum(last_n) / SAMPLE_SIZE

                # get note number and nearest note
                n = freq_to_number(this_avg)
                n0 = int(round(n))

                if note_name(n0) == self.wanted_note:
                    print('you got it right!!')
                    # increase pontuation
                    break #next_note

                print('wanted_note: {} freq: {:7.2f} Hz     note: {:>3s} {:+.2f}'.format(self.wanted_note, freq, note_name(n0), n-n0)) 
            
            # if the player wants so, go to the next note (break)
            # TODO
            
def main():
    game = NoteChecker()
    game.note_checker()


if __name__ == "__main__":
    main()