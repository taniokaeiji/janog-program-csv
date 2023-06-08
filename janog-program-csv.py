import requests
from bs4 import BeautifulSoup

import datetime, locale, csv

url = 'https://www.janog.gr.jp/meeting/janog52/program-ja-timeline/'

def get_program_list(url):
    link_list = []

    res = requests.get(url)
    content = res.content
    soup = BeautifulSoup(content, 'html.parser')
    for link in soup.find_all('div', 'timeline-item-snippet'):
        if link.a is None:
            continue
        link_list.append(link.a["href"])

    return list(set(link_list))

def program_info(url):
    res = requests.get(url)
    content = res.content
    soup = BeautifulSoup(content, 'html.parser')

    meta_keywords = soup.find_all('meta', attrs={'name': 'keywords'})
    if meta_keywords[0].get('content') != 'JANOGプログラム':
        exit
    else:
        # keep page url
        link = url

        # get Time, Presenter
        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description.get('content')
        presenter, start_time, end_time = description.split('|')
        presenter = presenter.replace(')', ')\n')

        # get Program title
        title = soup.h1.string

        # get abstract
        content = soup.find('div', attrs={'class', 'entry-content cf'})
        content_abstract = content.find(id='toc1')
        abstract = content_abstract.find_next()
        abstract_text = ""
        while abstract.name == 'p':
            abstract_text += abstract.text + '\n'
            abstract = abstract.find_next()
            if abstract.name == 'h3':
                break
            if abstract.name == 'br':
                abstract_text += '\n'
                abstract = abstract.find_next()

        abstract = link + ""
        abstract += "\n\n■概要\n"
        abstract += abstract_text
        abstract += "\n■登壇者\n"
        abstract += presenter

        # get place
        content_place = content.find(id='toc2')
        place = content_place.find_next('p').text

        # get hold date
        content_date = content.find(id='toc3')
        hold_date_text = content_date.find_next('p').text.split(' ')[1]
        locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
        hold_date = datetime.datetime.strptime(hold_date_text, '%Y年%m月%d日(%a)').strftime('%Y/%m/%d')

        return [title, hold_date, start_time, hold_date, end_time, place, abstract]

if __name__ == '__main__':
    links = get_program_list(url)
    events = []

    for link in links:
        event = program_info(link)
        events.append(event)

    # Write CSV
    header = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 'Location', 'Description']
    with open('janog-meeting-programs.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(header)
        for event in events:
            if event is None:
                continue
            writer.writerow(event)
