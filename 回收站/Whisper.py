import time
import openai
openai.api_key = "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"


def transcribe(file_name):
    audio_file = open(file_name, "rb")
    try:
        audio_file.read()  # 尝试读取文件内容
        print("File is open...")  # 如果能够读取，则文件已经被打开
    except FileNotFoundError:
        print("File is not open.")  # 如果文件未找到，则文件未被打开
        return 0
    audio_file.seek(0)  # f.read()读取文件指针会跑到文件的末端，如果再一次读取，读取的将是空格，所以要重定向文件指针
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print("Successfully converted...")
    time.sleep(1)
    return transcript.text


def askChatGPT(messages):
    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=1  # 可选参数，默认值为 1，取值 0-2。该值越大每次返回的结果越随机，即相似度越小。
    )
    return response['choices'][0]['message']['content']


def GPT_generate(text, prompt):
    messages = [{"role": "system", "content": prompt}]
    print("Prompt import successfully...")
    time.sleep(1)
    try:
        d = {"role": "user", "content": text}
        messages.append(d)
        print("original_text import successfully...")
        time.sleep(1)
        print("Generating.", end='')
        text_return = askChatGPT(messages)
        for i in range(4):
            print(".", end="")
            time.sleep(1)
        print()
        return 'Summary：' + '\n' + text_return + '\n'
    except:
        messages.pop()
        print('failed...')


def write_output(text):
    file = open("result.txt", "w")
    # 写入一段文字
    file.write(text)
    # 关闭文件
    file.close()


def main():
    file_name = "temp.m4a"
    prompt = "假设你是一个英语老师，你需要针对我给你的文章进行总结并概括，用中文告诉我"
    original_text = transcribe(file_name)
    if original_text == 0:
        print("fail to convert")
    summary_text = GPT_generate(original_text, prompt)
    text_to_be_written = ""
    text_to_be_written = text_to_be_written + "-------------------------------------------\n"
    text_to_be_written = text_to_be_written + "Original text:" + "\n" + original_text
    text_to_be_written = text_to_be_written + "\n-------------------------------------------\n"
    text_to_be_written = text_to_be_written + summary_text
    write_output(text_to_be_written)


if __name__ == "__main__":
    main()

