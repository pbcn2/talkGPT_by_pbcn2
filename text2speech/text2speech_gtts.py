from langdetect import detect
from gtts import gTTS
import pygame


class TextToSpeech:
    def __init__(self, filename, generate_audio_path):
        self.filename = filename
        self.read(generate_audio_path)

    def detect_language(self, text):
        """
        使用Python内置的language-detector库检测文本的语言
        """
        return detect(text)

    def read(self, generate_audio_path):
        """
        读取文件并使用Google TTS API将内容转换为语音输出
        """
        with open(self.filename, 'r', encoding="UTF-8") as f:
            text = f.read()

        # 检测语言
        language = self.detect_language(text)

        try:
            # 将文本转换为语音
            tts = gTTS(text, lang=language)
            tts.save(generate_audio_path)
        except:
            print("Failed to connect to Google_TTS...")
            return

        # # 播放语音
        # playsound('audio.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load(generate_audio_path)
        pygame.mixer.music.play(loops=1)
        while pygame.mixer.music.get_busy():
            pass
        # 停止音频文件播放
        pygame.mixer.music.stop()

        # 释放音频系统和所有已加载的音频文件
        pygame.mixer.quit()

        pygame.quit()

