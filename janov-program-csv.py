import requests
from bs4 import BeautifulSoup

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

        # get Program title
        title = soup.h1.string
        print(title)

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

        #print(abstract_text)

        # get place
        content_place = content.find(id='toc2')
        place = content_place.find_next('p').text
        #print(place)

        # get hold date
        content_date = content.find(id='toc3')
        hold_date = content_date.find_next('p').text.split(' ')[1]
        print(hold_date)

if __name__ == '__main__':
    links = get_program_list(url)
    for link in links:
        program_info(link)
        break