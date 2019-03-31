import os
from utils import compare_name, contains_any, find_most_dense_region

# Keywords to use while retrieving data from report grouped by its meaning
keywords = [
    {
        'securities beneficially owned by',
        'common stock beneficially owned by',
        'shares beneficially owned',
        'of beneficial owner',
        'beneficial ownership of',
        'certain beneficial ownership',
        'name of beneficial owner',
        'ownership of certain beneficial owners',
    },

    {
        'security ownership of certain',
        'securities ownership of certain',
        'security ownership of principal',
        'stock ownership of certain',
        'stock ownership of certain',
        'stock ownership of principal',
        'stock ownership of principal',
        'of our stock ownership',
        'security ownership of management',
        'ownership of our common shares',
    },

    {
        'the following table',
        'the table below',
    },

    {
        'principal shareholders',
        'principal stockholders',
        'ownership percentage',
        'major stockholders',
    },

    {
        'more than 5%',
        'more than five percent',
        '5% or more',
        'five percent or more',
    },

    {
        'of voting common stock',
        'of our voting common stock',
        'of our common stock',
    },

    {
        'blackrock',
        'vanguard',
    }
]

most_relevant_keywords = {
    'more than 5%',
    'more than five percent',
    '5% or more',
    'five percent or more',
}

not_found = lambda x, y: x == -1 and y == -1

keywords_hits = {}
for group in keywords:
    for kw in group:
        keywords_hits[kw] = 0

if __name__ == '__main__':
    files = sorted(os.listdir('data'), key=compare_name)

    for file_index, filename in enumerate(files):

        if file_index > 100: break

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

        margin = len(lines) // 10
        lines = lines[margin:]
        count, start, end = find_most_dense_region(lines, keywords, keywords_hits, most_relevant_keywords)

        end_line = lines[end - 1]
        while not (contains_any([end_line], ["<table>", "</table>"])) and end < len(lines):
            end += 1
            end_line = lines[end - 1]

        end += 40

        # start_line = lines[start - 1]
        # while not (contains_any([start_line], ["<table>", "</table>"])) and start >= len(lines):
        #     start -= 1
        #     start_line = lines[start - 1]

        print("{}: {}".format(filename, count))

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

    print("--- Keywords hits ---")
    for (kw, hits) in keywords_hits.items():
        print("{}: {}".format(kw, hits))
