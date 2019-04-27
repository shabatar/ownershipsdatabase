import os
import configparser
from utils import compare_name, find_most_dense_region, extend_until_table_ends, not_found

if __name__ == '__main__':
    # Keywords to use while retrieving data from report grouped by its meaning
    keywords = []
    curr_group = []
    config_path = os.path.join(os.path.curdir, 'config')
    data_path = os.path.join(os.path.curdir, 'data')
    dataCut_path = os.path.join(os.path.curdir, 'dataCut')
    with open(os.path.join(config_path, 'keywords.txt')) as keywords_file:
        line = keywords_file.readline()
        while line:
            if "------" in line:
                keywords.append(set(curr_group))
                curr_group = []
            elif not line.isspace():
                curr_group.append(line.strip())
            line = keywords_file.readline()
    if len(curr_group) > 0:
        keywords.append(set(curr_group))

    most_relevant_keywords = set()
    with open(os.path.join(config_path, 'most_relevant_keywords.txt')) as keywords_file:
        line = keywords_file.readline()
        while line:
            if not line.isspace():
                most_relevant_keywords.add(line.strip())
            line = keywords_file.readline()

    print(keywords)
    print(most_relevant_keywords)

    config = configparser.ConfigParser()
    config.read(os.path.join(config_path, 'settings.txt'))
    config = config['DEFAULT']
    reports_start = int(config['ReportsStart']) - 1  # config indices from 1, not from 0
    reports_end = int(config['ReportsEnd']) - 1
    region_size = int(config['RegionSize'])
    end_margin = int(config['EndMargin'])
    start_skip_percent = float(config['StartSkipPercent'])
    extend_until_table = config['ExtendUntilTable'] != 'no'

    files = sorted(os.listdir(data_path), key=compare_name)
    reports_end = min(reports_end, len(files))

    for filename in files[reports_start:reports_end+1]:
        try:
            file = open(os.path.join(data_path, filename), 'r', encoding='windows-1252')
        except IsADirectoryError:
            continue

        lines = [line for line in file]

        # split too long lines into several once by "<div" separator
        if len(lines) < 100:
            long_line = ""
            for i, line in enumerate(lines):
                if len(line) > 1000:
                    long_line += line + "\n"

            lines = long_line.replace("<div", "\n<div").split("\n")

        start_margin = int(len(lines) * start_skip_percent)
        lines = lines[start_margin:]
        count, start, end = find_most_dense_region(lines, keywords, most_relevant_keywords, region_size)

        if extend_until_table:
            end = extend_until_table_ends(end, lines)

        end += end_margin

        # print("{}: {}".format(filename, count))
        print("{}: processed".format(filename))

        if not_found(start, end):
            file.close()
            continue

        if not os.path.exists(dataCut_path):
            os.mkdir(dataCut_path)
        fileCut = open(os.path.join(dataCut_path, filename), 'w', encoding='windows-1252')
        file.seek(0)
        for line in lines[start:end]:
            fileCut.write(line)
        fileCut.close()
        file.close()

    # print("--- Keywords hits ---")
    # for (kw, hits) in keywords_hits.items():
    #     print("{}: {}".format(kw, hits))
