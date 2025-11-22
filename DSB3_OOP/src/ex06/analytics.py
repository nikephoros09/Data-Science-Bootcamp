import os
from random import randint
import logging
import requests

logging.basicConfig(
    filename='analytics.log',
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s,%(msecs)03d %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

class Research:
    def __init__(self, file_path):
        self.file_path = file_path
        logging.debug(f'The following file is being processed - {file_path}')

    def file_reader(self, has_header=True):
        logging.debug('Validation and output preparation')
        with open(self.file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        if not lines:
            logging.error('Wrong file structure')
            raise Exception("Wrong file structure")

        start = 0
        if has_header:
            header = lines[0].split(',')
            if len(header) != 2 or not header[0] or not header[1]:
                logging.error('Wrong file structure')
                raise Exception("Wrong file structure")
            start = 1

        allowed_values = {"0", "1"}
        result = []

        for line in lines[start:]:
            columns = [item.strip() for item in line.split(',')]
            if len(columns) != 2 or not all(c in allowed_values for c in columns):
                logging.error('Wrong file structure')
                raise Exception("Wrong file structure")
            if columns[0] == columns[1]:
                logging.error('Wrong file structure')
                raise Exception("Wrong file structure")
            result.append([int(columns[0]), int(columns[1])])

        if not result:
            logging.error('Wrong file structure')
            raise Exception("Wrong file structure")

        return result

    @staticmethod
    def tg_message(report_created, token):

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        if report_created:
            message = "The report has been successfully created."
        else:
            message = "The report hasn't been created due to an error."
        payload = {
            'chat_id': 1963270813,
            'text': message,
        }
        
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            logging.debug('Telegram message sent successfully')
        else:
            logging.error('Failed to send message to Telegram')

    class Calculations:
        def __init__(self, data):
            self.data = data
            logging.debug(f'Calculations are in process')

        def counts(self):
            heads = sum(row[0] for row in self.data)
            tails = sum(row[1] for row in self.data)
            logging.debug(f'Counted heads and tails - {heads}, {tails}')

            return heads, tails

        def fractions(self, heads, tails):
            total = heads + tails
            heads_percent = heads / total
            tails_percent = tails / total
            logging.debug(f'Calculated fractions of heds and tails - {heads_percent:.4f}, {tails_percent:.4f}')
            return round(heads_percent, 4), round(tails_percent, 4)

    class Analytics(Calculations):
        def predict_random(self, num_predictions):
            result = []
            for _ in range(num_predictions):
                item = randint(0, 1)
                result.append([item, 1-item])
            logging.debug(f'Series of flips prediction - {result}')
            return result

        def predict_last(self):
            last = self.data[-1]
            logging.debug(f'Last flip prediction - {last}')
            return last

        @staticmethod
        def save_file(data, filename, extension):
            full_name = f"{filename}.{extension}"
            with open(full_name, "w") as file:
                file.write(str(data))
            logging.debug(f'The result is saved in {full_name}')