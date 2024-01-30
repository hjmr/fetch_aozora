import os
from bs4 import BeautifulSoup
import requests
import re


def get_author_page_url(author):
    base_url = "https://www.aozora.gr.jp/index_pages/"
    res = requests.get(base_url + "person_all.html")
    soup = BeautifulSoup(res.text.encode(res.encoding), "html.parser")
    author_link = soup.find("a", text=author)
    href = None
    if author_link is not None:
        href = base_url + author_link.get("href").split("#")[0]
    return href


def get_author_works_urls(author):
    base_url = "https://www.aozora.gr.jp/"
    url_regex = re.compile(r"cards\/.+\.html$")

    author_url = get_author_page_url(author)
    works_urls = {}
    if author_url is not None:
        res = requests.get(author_url)
        soup = BeautifulSoup(res.text.encode(res.encoding), "html.parser")
        works_links = soup.find_all("a", {"href": url_regex})
        if works_links is not None:
            for w in works_links:
                w_title = w.text
                w_url = base_url + url_regex.search(w.get("href")).group()
                works_urls[w_title] = w_url
    return works_urls


def get_author_work_page_url(author, work):
    works_urls = get_author_works_urls(author)
    url = None
    if work in works_urls.keys():
        url = works_urls[work]
    return url


def get_author_work_url(author, work):
    work_page_url = get_author_work_page_url(author, work)
    url = None
    if work_page_url is not None:
        res = requests.get(work_page_url)
        soup = BeautifulSoup(res.text.encode(res.encoding), "html.parser")
        dl_tag = soup.find("table", class_="download")
        if dl_tag is not None:
            xhtml_tag = dl_tag.find("a", {"href": re.compile(r"\.html$")})
            if xhtml_tag is not None:
                url = xhtml_tag.get("href")
    if url is not None:
        url = os.path.dirname(work_page_url) + "/files/" + os.path.basename(url)
    return url


def get_author_work_content(author, work):
    work_url = get_author_work_url(author, work)
    content = None
    if work_url is not None:
        res = requests.get(work_url)
        soup = BeautifulSoup(res.text.encode(res.encoding), "html.parser")
        content_tag = soup.find("div", class_="main_text")
        if content_tag is not None:
            content = content_tag.decode_contents()
    return content


if __name__ == "__main__":
    w = get_author_work_content("太宰 治", "パンドラの匣")
    print(w)
