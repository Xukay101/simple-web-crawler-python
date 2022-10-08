import logging, sys, os

from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment
from hashlib import sha256
from shutil import rmtree

logging.basicConfig(level=logging.INFO)

init_url = sys.argv[1]
limit_depth = int(sys.argv[2])

urls = []
def crawler(url, depth=0):
    if depth > limit_depth:
        return

    # Obtener los datos
    try:
        session = urlopen(url) 
        soup = BeautifulSoup(session.read(), 'html.parser')
        session.close()
    except:
        logging.warning(f'CONNECT: Fail in {url[:50]}...')
        return []

    # Limpir los datos
    [x.extract() for x in soup.find_all('script')]
    [x.extract() for x in soup.find_all('style')]
    [x.extract() for x in soup.find_all('meta')]
    [x.extract() for x in soup.find_all('noscript')]
    [x.extract() for x in soup.find_all(text=lambda text:isinstance(text, Comment))]

    # Obtener links
    links = []
    for link in soup.find_all('a'):
        link = link.get('href')
        if str(link)[0:5] == 'https' and str(link) not in urls:
            links.append(link)
    logging.info(f'CONNECT: {len(links)} links in {url[:50]}...')

    # Guardar el contenido en html
    html = soup.prettify('utf-8')
    name_file = sha256(url.encode('utf-8')).hexdigest()
    with open(f'./data/{name_file}.html', "w") as file:
        file.write(str(html))

    for link in links:
        urls.append(link)
        crawler(link, depth+1)

if __name__ == '__main__':
    try:
        rmtree('./data', ignore_errors=False, onerror=None)
    except: pass
    os.mkdir('data')
    crawler(init_url)
    with open('./urls.txt', 'w') as file:
        for url in urls:
            file.write(url)