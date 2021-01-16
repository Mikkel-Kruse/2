from multiprocessing import Process
import speech_recognition as sr


class SpeechCommander:

    def __init__(self, queue):
        self.speech_recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.queue = queue
        self.start_commander()

    def act_on_voice_command(self):
        while True:
            with self.microphone as source:
                self.speech_recognizer.adjust_for_ambient_noise(source)
                #data = r.record(source, duration=4)
                data = self.speech_recognizer.listen(source)
                #text = r.recognize_google(data, language='en-US')
                text = self.speech_recognizer.recognize_google(data, language='en-IN', show_all=True)

            if 'walk' in str(text):
                self.queue.put(text)
            elif 'stop' in str(text):
                self.queue.put(text)
            else:
                self.queue.put(text)

    def start_commander(self):
        p = Process(target=self.act_on_voice_command, args=())
        p.daemon = True
        p.start()


if __name__ == '__main__':
    queue = 0
    speech = SpeechCommander(queue)
