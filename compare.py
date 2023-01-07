import ast
import argparse


class Interface:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Compare files')
        parser.add_argument('input_file', type=str, help='Input file')
        parser.add_argument('output_file', type=str, help='Output file')
        args = parser.parse_args()
        self.input_file_path, self.output_file_path = args.input_file, args.output_file
        self.dict_compare_files = {}
        self.output_values = []

    def read_input_file(self):
        with open(self.input_file_path) as input_file:
            for index, line in enumerate(input_file):
                files = line.split()
                self.dict_compare_files[index] = [
                    File(files[0]),
                    File(files[1]),
                ]

    def compare_files(self):
        for values in self.dict_compare_files.values():
            self.output_values.append(
                1 - self.levenstein_algorithm(File.unparse_file(values[0].open_file()),
                                              File.unparse_file(values[1].open_file())) / len(values[0]))

    def write_output_file(self):
        with open(self.output_file_path, 'w') as output_file:
            for value in self.output_values:
                output_file.write(str(round(value, 2)) + '\n')
            print('done')

    @staticmethod
    def levenstein_algorithm(str_1, str_2):
        n, m = len(str_1), len(str_2)
        if n > m:
            str_1, str_2 = str_2, str_1
            n, m = m, n
        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if str_1[j - 1] != str_2[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)
        return current_row[n]


class File:
    def __init__(self, path):
        self.path = path

    def open_file(self):
        with open(self.path) as f:
            return self.parse_file(f.read())

    @staticmethod
    def parse_file(file):
        return ast.parse(file)

    @staticmethod
    def unparse_file(file):
        return ast.unparse(file)

    def __len__(self):
        with open(self.path) as f:
            return len(ast.unparse(ast.parse(f.read())))


interface = Interface()
interface.read_input_file()
interface.compare_files()
interface.write_output_file()
