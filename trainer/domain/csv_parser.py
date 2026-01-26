from typing import List

from entity.Feedback import Feedback


class CSV_parser:

    def __set_header(self, output_csv_path: str):
        with open(output_csv_path, 'w', encoding='utf-8') as f:
            f.write('text;label\n')
 
    def parse(self, feedback_sql_result: List[Feedback], output_csv_path: str):
        self.__set_header(output_csv_path)
        idx, chunk_size, length = 0, 1000, len(feedback_sql_result)
        while idx < length:
            chunk_size = min(chunk_size, length - idx)
            for f in feedback_sql_result[idx: idx + chunk_size]:
                self.__process_feedback(f, output_csv_path)
            idx += chunk_size

    def __process_feedback(self, feedback: Feedback, output_csv_path: str):
        with open(output_csv_path, 'a', encoding='utf-8') as f:
            line = feedback.message_text + ';' + str(feedback.feedback_result) + '\n'
            f.write(line)
    