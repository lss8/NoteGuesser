
import numpy as np
import pyaudio
import random
import wave


# declare constants
NOTE_MIN = 60       # C4
NOTE_MAX = 69       # A4
FSAMP = 22050       # Sampling frequency in Hz
FRAME_SIZE = 2048   # How many samples per frame?
FRAMES_PER_FFT = 16 # FFT takes average across how many frames?
RATE = 44100  # Recording rate


# Number of data points to average over. This is used for 2 things
# 1. Reducing noise between subsequent string strokes
# 2. We don't output too many values which might confuse the user
SAMPLE_SIZE = 8

SAMPLES_PER_FFT = FRAME_SIZE*SAMPLE_SIZE
FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT

NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()


def freq_to_number(f): return 69 + 12*np.log2(f/440.0)
def number_to_freq(n): return 440 * 2.0**((n-69)/12.0)
def note_name(n): return NOTE_NAMES[n % 12]

def note_to_fftbin(n): return number_to_freq(n)/FREQ_STEP
imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN-1))))
imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX+1))))

class NoteGuesser:
    
    notes_to_check = 'C D E F G A B'.split()

    def open_audio(self):
    # open stream to wait for sound
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

    
    def switch_note(self, note):
        self.wanted_note = note
        print(f"Now this note: {note}")
    
    def note_guess(self):
        self.open_audio()
        random.shuffle(self.notes_to_check)
        
        # decide wanted note
        for n in self.notes_to_check:
            self.switch_note(n)
            self.uke_loop()
        
        self.close_audio()
       
        
    def uke_loop(self):
        num_frames = 0
        last_n = [0] * SAMPLE_SIZE
        last_avg = 1
        buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
        window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))

        while True:

            buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
            buf[-FRAME_SIZE:] = np.fromstring(self.stream.read(FRAME_SIZE), np.int16)

            # Run the FFT 
            fft = np.fft.rfft(buf*window)
           
            freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP
            
            # Get note number and nearest note
            n = freq_to_number(freq)
            n0 = int(round(n))

            # Console output once we have a full buffer
            last_n[num_frames] = int(freq)
            num_frames += 1

            if num_frames == SAMPLE_SIZE:
                num_frames = 0
               
                if note_name(n0) == self.wanted_note:
                    print('you got it right!!')
                    #break #next_note

            print('wanted_note: {} freq: {:7.2f} Hz     note: {:>3s} {:+.2f}'.format(self.wanted_note, freq, note_name(n0), n-n0)) 
            # if got it right, go to the next note
            '''
            # if the person gives up, go to the next note (break)
            if input("Do you wanna give up? [Y/N]") == "Y":
                break
            '''          
def main():
    game = NoteGuesser()
    game.note_guess()


if __name__ == "__main__":
    main()