import os
import configparser
from src.utils import compare_name, find_most_dense_region, extend_until_table_ends

if __name__ == '__main__':
    # Keywords to use while retrieving data from report grouped by its meaning
    keywords = []
    with open("./config/keywords.txt") as keywords_file:
        curr_group = []
        line = keywords_file.readline()
        while line:
            if "------" in line:
                keywords.append(set(curr_group))
                curr_group = []
            elif not line.isspace():
                curr_group.append(line)
            line = keywords_file.readline()

    most_relevant_keywords = set()
    with open("./config/most_relevant_keywords.txt") as keywords_file:
        line = keywords_file.readline()
        while line:
            if not line.isspace():
                most_relevant_keywords.add(line)
            line = keywords_file.readline()

    print(keywords)
    print(most_relevant_keywords)

    config = configparser.ConfigParser()
    config.read('./config/settings.txt')
    reports_count = config['ReportsCount']
    region_size = config['RegionSize']
    end_margin = config['EndMargin']
    start_skip = config['StartSkip']
    extend_until_table = config['ExtendUntilTable']

    files = sorted(os.listdir('data'), key=compare_name)

    for file_index, filename in enumerate(files)[:reports_count]:
        try:
            file = open('data/' + filename, 'r', encoding='windows-1252')
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

        start_margin = len(lines) * start_skip
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
        if not os.path.exists('dataCut'):
            os.mkdir('dataCut')
        fileCut = open('dataCut/' + filename, 'w', encoding='windows-1252')
        file.seek(0)
        for line in lines[start:end]:
            fileCut.write(line)
        fileCut.close()
        file.close()

    # print("--- Keywords hits ---")
    # for (kw, hits) in keywords_hits.items():
    #     print("{}: {}".format(kw, hits))
