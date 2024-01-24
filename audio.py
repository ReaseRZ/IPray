import wave
import time
import sys
import keyboard
import pyaudio
import threading

class Audio(threading.Thread):
    def __init__(self,filename):
        self.wf = wave.open(filename, 'rb')
        self.pAudio = pyaudio.PyAudio()
        self.stream = None
        self.data = None

    def PlayAudio(self):
        self.stream =  self.pAudio.open(format=self.pAudio.get_format_from_width(self.wf.getsampwidth()),
                        channels=self.wf.getnchannels(),
                        rate=self.wf.getframerate(),
                        output=True)
       # Read data in chunks
        self.data = self.wf.readframes(1024)

        # Play the sound by writing the audio data to the stream
        while self.data != '':
            self.stream.write(self.data)
            self.data = self.wf.readframes(1024)
                
    def StopAudio(self,args):
        print('Success')
        self.stream.stop_stream()
        self.stream.close()
        self.pAudio.terminate()
