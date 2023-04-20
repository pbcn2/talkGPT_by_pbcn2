import pyaudio
import wave
import threading
import logging


class AudioRecorderPlayer:
    def __init__(self, filename, output_device_index=3):
        self.CHUNK = 1024  # 每个缓存块的大小
        self.FORMAT = pyaudio.paInt16  # 采样格式
        self.CHANNELS = 1  # 声道数量
        self.RATE = 44100  # 采样率

        # 创建 PyAudio 对象
        self.p = pyaudio.PyAudio()

        # 初始化状态变量
        self.recording = False
        self.frames = []
        self.recording_thread = None

        # 创建输出对象
        self.pForOutput = pyaudio.PyAudio()

        self.output_device_index = output_device_index

        self.main(filename)

    # 定义录音线程
    def record(self):
        self.frames = []  # 用于存储录音数据
        # 打开音频流，启动录音功能
        stream = self.p.open(format=self.FORMAT,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             input=True,
                             frames_per_buffer=self.CHUNK)
        # 录音过程中将音频流的数据写入缓存块
        while self.recording:
            data = stream.read(self.CHUNK)
            self.frames.append(data)
        # 停止录音并关闭音频流
        stream.stop_stream()
        stream.close()

    # 定义播放函数
    def play_audio(self, filename):
        # 打开音频文件
        wf = wave.open(filename, 'rb')
        # 创建音频流并启动音频播放
        stream = self.pForOutput.open(format=self.pForOutput.get_format_from_width(wf.getsampwidth()),
                                      channels=wf.getnchannels(),
                                      rate=wf.getframerate(),
                                      output=True,
                                      output_device_index=self.output_device_index)
        # 读取并播放帧数据
        data = wf.readframes(self.CHUNK)
        while data:
            stream.write(data)
            data = wf.readframes(self.CHUNK)
        # 停止流和 PyAudio 对象
        stream.stop_stream()
        stream.close()
        wf.close()

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.recording_thread = threading.Thread(target=self.record)
            self.recording_thread.start()
            print("开始录音...")
        else:
            print("录音已经开始了！")

    def stop_recording(self, filename):
        if self.recording:
            self.recording = False
            self.recording_thread.join()
            print("录音结束！")
            # 将录音数据写入 WAV 文件
            wf = wave.open(filename, "wb")
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b"".join(self.frames))
            wf.close()
        else:
            print("没有正在录音！")

    def quit(self):
        if self.recording:
            self.recording = False
            self.recording_thread.join()
        self.p.terminate()
        self.pForOutput.terminate()

    def main(self, filename):
        while True:
            self.start_recording()
            user_input = input("输入 's' 停止录音并保存：")
            # if user_input == 'r':
            #     self.start_recording()
            if user_input == 's':
                self.stop_recording(filename)
                self.quit()
                logging.info("successfully recorded and saved!")
                break
            elif user_input == 'p':
                self.play_audio(filename)
            elif user_input == 'q':
                self.quit()
                break
            else:
                print("无效的输入！")


if __name__ == '__main__':
    audio_player = AudioRecorderPlayer("audio.wav")
