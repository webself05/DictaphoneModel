import time
import numpy as np

import sounddevice as sd
import soundfile as sf
import os

class Recorder:
    def __init__(self, memory, battery, power):
        self.memory = memory
        self.battery = battery
        self.power = power

        self.recording = False
        self.playing = False
        self.paused = False
        self.current_play_msg = None

        if not os.path.exists("recordings"):
            os.mkdir("recordings")

    def start_recording(self, samplerate=44100):
        if self.power.is_save_mode():
            return "Невозможно записывать в режиме энергосбережения"
        self.audio_buffer =[]
        self.recording = True
        self.battery.drain(2)
        self.samplerate = samplerate

        self.record_start_time = time.time()

        def callback(indata,frames,time_info,status):
            if self.recording:
                self.audio_buffer.append(indata.copy())

        self.stream = sd.InputStream(
            callback = callback,
            channels = 1,
            samplerate = self.samplerate
        )
        self.stream.start()
        return "Запись началась"

    def stop_recording(self):
        if not self.recording:
            return "Запись не велась"

        self.recording = False
        self.stream.stop()

        duration = int(time.time() - self.record_start_time)

        msg_id = len(self.memory.messages) + 1
        filename = f"recordings/message_{msg_id}.wav"

        if len(self.audio_buffer) == 0:
            return "Ошибка: нет записанных данных"

        audio_np = np.concatenate(self.audio_buffer, axis=0)

        sf.write(filename, audio_np, self.samplerate)

        success, msg = self.memory.add_message(duration, filename)
        return msg

    def start_playback(self, msg_id):
        if self.power.is_save_mode():
            return "Воспроизведение запрещено"

        msg = self.memory.get_message(msg_id)
        if not msg:
            return "Сообщение не найдено"

        self.playing = True
        self.paused = False
        self.current_play_msg = msg

        print(f"Воспроизведение записи {msg_id}")

        data, samplerate = sf.read(msg["content"])

        if len(data.shape) > 1:
            data = data[:, 0]

        sd.play(data, samplerate)
        sd.wait()
        self.battery.drain(1)

        self.playing = False
        return "Воспроизведение завершено"

    def pause(self):
        if self.playing:
            self.paused = True
            print("Пауза")
            return "Пауза"
        return "Не воспроизводится"

    def stop(self):
        self.recording = False
        self.playing = False
        self.paused = False
        return "Остановлено"