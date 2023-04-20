import csv
import logging
import os

from AudioRecorder.audio_recorder_player import AudioRecorderPlayer
from audio2text.audio_to_text import AudioToText
from text2respond.ask_for_respond import AskForRespond
from text2respond.add_txt_to_csv_log import AddTXT2MessageLog
from text2speech.text2speech_gtts import TextToSpeech

logging.disable(logging.CRITICAL + 1)
# logging.basicConfig(level=logging.INFO)


def initialize(api_key, prompt, message_log_path):
    def save_dict_list_to_csv(dict_list, filename):
        """
        将字典列表保存为CSV文件
        dict_list: 字典列表
        filename: 文件名
        """
        with open(filename, mode='w', newline='') as f:
            fieldnames = list(dict_list[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for my_dict in dict_list:
                writer.writerow(my_dict)
    # 指定log文件路径
    log_path = message_log_path
    messages = [{"role": "system", "content": prompt}]
    save_dict_list_to_csv(messages, log_path)
    logging.debug("successfully initialized message_log!")
    AskForRespond(api_key, log_path, "text2respond/generate_text.txt")
    logging.debug("successfully received initialization reply!")


def loop(api_key, audio_path, txt_path, message_log_path, generate_text_path, generate_audio_path):
    while True:
        record(audio_path)  # 录入回答
        turnTXT(api_key, audio_path, txt_path)  # 转文字
        appendMessageLog(message_log_path, txt_path, role="user")  # 将新回答append进message_log等待传入API
        ask_API(api_key, message_log_path, generate_text_path)  # 将回答传给API并取得回答，将回答输出并写入message_log
        read_txt(generate_text_path, generate_audio_path)
        logging.info("------A Loop Is Over------")

        # 询问是否继续
        while True:
            response = input("是否继续？(l继续/e结束)")
            if response == 'l':
                break
            elif response == 'e':
                return  # 直接结束程序
            else:
                print("请输入有效指令！")


def record(audio_path):
    AudioRecorderPlayer(audio_path)


def turnTXT(api_key, audio_path, txt_path):
    AudioToText(api_key, audio_path, txt_path)


def appendMessageLog(message_log_path, txt_path, role="user"):
    AddTXT2MessageLog(message_log_path, txt_path, role)  # 将user说的话添加进message中等待传给API


def ask_API(api_key, message_log_path, generate_text_path):
    AskForRespond(api_key, message_log_path, generate_text_path)  # 将文件传给API等待回传结果


def read_txt(generate_text_path, generate_audio_path):
    TextToSpeech(generate_text_path, generate_audio_path)
    os.remove(generate_audio_path)


def main():
    prompt = "hello"
    api_key = "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"
    audio_path = "AudioRecorder/audio.wav"
    message_log_path = "text2respond/message.csv"
    txt_path = "audio2text/text.txt"
    generate_text_path = "text2respond/generate_text.txt"
    generate_audio_path = "text2speech/generate_audio.mp3"

    initialize(api_key, prompt, message_log_path)  # 初始化系统

    loop(api_key, audio_path, txt_path, message_log_path, generate_text_path, generate_audio_path)  # 启动问答循环


if __name__ == "__main__":
    main()
