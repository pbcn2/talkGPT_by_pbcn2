
import openai
import csv
import sys
import logging


class AskForRespond:
    def __init__(self, api_key, message_file_path, generate_text_path):
        self.api_key = api_key
        openai.api_key = api_key
        self.MODEL = "gpt-3.5-turbo"
        self.main(message_file_path, generate_text_path)

    def askChatGPT(self, messages):
        response = openai.ChatCompletion.create(
            model=self.MODEL,
            messages=messages,
            temperature=1)
        return response['choices'][0]['message']['content']

    @staticmethod
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

    @staticmethod
    def load_dict_list_from_csv(filename):
        """
        从CSV文件中恢复字典列表
        filename: 文件名
        return: 字典列表
        """
        try:
            dict_list = []
            with open(filename, mode='r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    dict_list.append(row)
            return dict_list
        except:
            sys.exit(-102)

    @staticmethod
    def check_last_role(lst):
        last_element = lst[-1]
        role_value = last_element['role']
        if role_value not in ['user', 'system']:
            return False
        else:
            return True

    def main(self, file_name, generate_text_path):
        chat_log = self.load_dict_list_from_csv(file_name)
        if self.check_last_role(chat_log):
            resp = self.askChatGPT(chat_log)
            logging.info("successfully received a response!")
            # 打开一个txt文件，如果该文件不存在，将会被创建
            file = open(generate_text_path, "w", encoding="UTF-8")
            # 写入文本内容
            file.write(resp)
            # 关闭文件
            file.close()
            print(resp)
            response = {"role": "assistant", "content": resp}
            chat_log.append(response)
            self.save_dict_list_to_csv(chat_log, file_name)
            logging.info("successfully appended the message_log!")
        else:
            sys.exit(-101)


# 测试主函数
if __name__ == "__main__":
    api_key = "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"
    asker = AskForRespond(api_key, )
    asker.main()

