import csv


class Splitter:
    def __init__(self, file_name: str):
        self.file_name = file_name

    def create_csv_by_years(self, years, list_naming):
        for year in years:
            with open(f"stats_by_year/{year}.csv", mode="w", encoding='utf-8') as w_file:
                file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
                file_writer.writerow(list_naming)
                for row in years[year]:
                    file_writer.writerow(row)

    def find_same_line_yrs(self):
        yrs = {}
        with open(self.file_name, encoding='utf-8-sig') as my_f:
            fr = csv.reader(my_f, delimiter=",")
            count = 0
            for line in fr:
                if (count == 0):
                    count += 1
                    arr_name = line
                else:
                    if ("" in line or len(line) != len(arr_name)):
                        continue
                    year = line[5][0:4]
                    if year not in yrs.keys():
                        yrs[year] = list()
                    yrs[year].append(line)
        return (yrs, arr_name)

    def split_my_file(self):
        (yrs, arr_name) = self.find_same_line_yrs()
        self.create_csv_by_years(yrs, arr_name)
        return 10



fName = input("Введите название csv-исходника: ")
spliter = Splitter(fName)
spliter.split_my_file()