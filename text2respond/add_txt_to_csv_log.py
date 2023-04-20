import csv
import sys
import logging


class AddTXT2MessageLog:
    def __init__(self, message_log_path, txt_file_path, role="user"):
        self.message_log_path = message_log_path
        self.filename = txt_file_path

        # 打开转文字所得并读取所有内容
        with open(self.filename, 'r') as file:
            file_contents = file.read()

        # 将文件内容插入到字典的content键对应的值中
        t = {"role": role, "content": file_contents}
        logging.info("successfully created new response_dict!")

        # 将字典添加到CSV文件中
        message = self.load_dict_list_from_csv()
        logging.info("successfully read the message_log!")
        message.append(t)
        self.save_dict_list_to_csv(message)
        logging.info("successfully written the message_log!")

    def save_dict_list_to_csv(self, dict_list):
        """
        将字典列表保存为CSV文件
        dict_list: 字典列表
        """
        with open(self.message_log_path, mode='w', newline='') as f:
            fieldnames = list(dict_list[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for my_dict in dict_list:
                writer.writerow(my_dict)

    def load_dict_list_from_csv(self):
        """
        从CSV文件中恢复字典列表
        return: 字典列表
        """
        try:
            dict_list = []
            with open(self.message_log_path, mode='r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    dict_list.append(row)
            return dict_list
        except:
            sys.exit(-102)
