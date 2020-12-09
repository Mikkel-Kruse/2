# This is a sample Python script.
from threading import Thread
from multiprocessing import Process
import speech_recognition as sr


#class SpeechCommander:

 #   def __init__(self):
  #      self.speech_recognizer = sr.Recognizer()
   #     self.microphone = sr.Microphone()

def act_on_voice_command(microphone, speech_recognizer):
    while True:
        with microphone as source:
            speech_recognizer.adjust_for_ambient_noise(source)
            #data = r.record(source, duration=4)
            data = speech_recognizer.listen(source)
            #text = r.recognize_google(data, language='en-US')
            text = speech_recognizer.recognize_google(data, language='en-IN', show_all=True)
            print(str(text))

        if 'walk' in str(text):
            print('ok')
            moving_right = True
        elif 'stop' in str(text):
            print('ok s')
            moving_right = False
        else:
            print('false')


if __name__ == '__main__':
    import speech_recognition as sr

    mic = sr.Microphone()
    speech = sr.Recognizer()
    speech_thread = Thread(target=act_on_voice_command, args=(mic, speech))
    speech_thread.start()
