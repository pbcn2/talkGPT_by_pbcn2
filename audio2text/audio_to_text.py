import time
import openai
import logging


class AudioToText:
    def __init__(self, api_key, audio_path, txt_path):
        self.api_key = api_key
        openai.api_key = api_key
        self.MODEL = "gpt-3.5-turbo"
        self.main(audio_path, txt_path)

    @staticmethod
    def transcribe(file_name):
        audio_file = open(file_name, "rb")
        try:
            audio_file.read()  # 尝试读取文件内容
            logging.info("File is open...")  # 如果能够读取，则文件已经被打开
        except FileNotFoundError:
            logging.info("Warning: File is not open.")  # 如果文件未找到，则文件未被打开
            return 0
        audio_file.seek(0)  # f.read()读取文件指针会跑到文件的末端，如果再一次读取，读取的将是空格，所以要重定向文件指针
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        logging.info("Successfully converted...")
        return transcript.text

    @staticmethod
    def write_output(text, txt_path):
        file = open(txt_path, "w")
        # 写入一段文字
        file.write(text)
        # 关闭文件
        file.close()

    def main(self, file_name, txt_path):
        original_text = self.transcribe(file_name)
        if original_text == 0:
            print("fail to convert")
        self.write_output(original_text, txt_path)
        logging.info("speech-to-text completed successfully!")


if __name__ == '__main__':
    api_key = "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"
    audio_path = "split.mp3"
    txt_path = "text.txt"
    text_summarizer = AudioToText(api_key, audio_path, txt_path)
