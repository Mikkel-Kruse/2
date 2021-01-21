from multiprocessing import Process
import speech_recognition as sr
import time


class SpeechCommander:

    def __init__(self, queue):
        self.speech_recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.stop_listening = 0
        self.queue = queue

    def act_on_voice_command(self, recognizer, audio):
        """
        while True:

            with self.microphone as source:
                self.speech_recognizer.adjust_for_ambient_noise(source)
                data = self.speech_recognizer.listen(source)
                """
        text = self.speech_recognizer.recognize_google(audio, language='en-IN', show_all=False)

        if 'walk' in str(text):
            #print(text)
            self.queue.put(text)
        elif 'stop' in str(text):
            #print(text)
            self.queue.put(text)
        else:
            #print(text)
            self.queue.put(text)

    def start_commander(self):
        with self.microphone as source:
            self.speech_recognizer.adjust_for_ambient_noise(source)
        self.speech_recognizer.pause_threshold = 0.8
        self.stop_listening = self.speech_recognizer.listen_in_background(self.microphone, self.act_on_voice_command)

    """
    def start_commander(self):
        p = Process(target=self.act_on_voice_command, args=())
        p.daemon = True
        p.start()
        p.join()
"""


if __name__ == '__main__':
    queue = 0
    speech = SpeechCommander(queue)
    speech.start_commander()
