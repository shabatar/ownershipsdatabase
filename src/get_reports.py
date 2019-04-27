import lxml.html
import pandas as pd
import requests
import os


def link(cik): return 'https://www.sec.gov/cgi-bin/browse-edgar?' + \
                      'action=getcompany&CIK={}&type=def+14A&dateb=&owner=exclude&count=40'.format(cik)


if __name__ == '__main__':
    csv_path = os.path.join(os.path.curdir, 'config', 'sp-500.csv')
    df = pd.read_csv(csv_path, sep=',', header=0)
    site = 'https://www.sec.gov'
    ciks = df['Symbol']
    names = list(df['Name'])

    for i, cik in enumerate(list(ciks)):
        response = requests.get(link(cik))
        tree = lxml.html.fromstring(response.text)

        urls = tree.xpath('//a/@href')
        url_names = tree.xpath("//a[text()=' Documents']/@href")

        try:
            report_site_url = url_names[0]
        except:
            report = ""
            err = '{} report not found'.format(names[i])
            print(err)
            continue

        report_response = requests.get(site + report_site_url)
        report_tree = lxml.html.fromstring(report_response.text)

        url_names = report_tree.xpath("//a[contains(text(), 'htm')]/@href")

        try:
            report = requests.get(site + url_names[0])
        except:
            report = ""
            err = '{} htm file not found'.format(names[i])
            print(err)
            continue

        res = '{} report successfully added'.format(names[i])
        print(res)

        data_path = os.path.join(os.path.curdir, 'data')

        if not os.path.exists(data_path):
            os.mkdir(data_path)

        formattedName = names[i].replace("/", "-").replace("\\", "-")

        file_path = os.path.join(data_path, "{}-{}.htm".format(i + 1, formattedName))
        file = open(file_path, "w")
        file.write(report.text)
        file.close()
