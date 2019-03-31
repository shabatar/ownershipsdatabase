import lxml.html
import pandas as pd
import requests
import os

if __name__ == '__main__':
    df = pd.read_csv('../config/sp-500.csv', sep=',', header=0)
    site = 'https://www.sec.gov'
    link = lambda \
            cik: 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=def+14A&dateb=&owner=exclude&count=40'.format(
        cik)
    ciks = df['Symbol']
    names = list(df['Name'])

    reports = []
    report = open('loading_report.txt', 'a+')
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

        reports.append(report)
        res = '{} report successfully added'.format(names[i])
        print(res)
        if not os.path.exists('../data'):
            os.mkdir('../data')

        formattedName = names[i].replace("/", "-").replace("\\", "-")

        file = open("../data/{}-{}.htm".format(i + 1, formattedName), "w")
        file.write(report.text)
        file.close()
        continue
