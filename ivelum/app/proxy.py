"""
Обработка HTML: добавление ™ к словам из 6 букв, замена ссылок и форм
на URL прокси, чтобы браузер оставался на адресе прокси.
"""
from bs4 import BeautifulSoup
from bs4.element import NavigableString

from app.config import settings
from app.utils.text import add_trademark


def _add_trademark_to_text_nodes(soup: BeautifulSoup) -> None:
    """Добавляет ™ после слов из 6 букв во всех текстовых узлах, кроме script/style."""
    for element in soup.find_all(text=True):
        if isinstance(element, NavigableString) and element.parent.name not in (
            "script",
            "style",
        ):
            new_text = add_trademark(str(element))
            element.replace_with(new_text)


def _is_hn_url(url: str, hn_base: str) -> bool:
    """Проверяет, что URL принадлежит Hacker News (защита от подмены хоста)."""
    return url == hn_base or url.startswith(hn_base + "/")


def _rewrite_links(
    soup: BeautifulSoup, proxy_url: str, hn_base: str
) -> None:
    """Заменяет href в ссылках на URL прокси (относительные и полные на HN)."""
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("/"):
            link["href"] = f"{proxy_url}{href}"
        elif _is_hn_url(href, hn_base):
            link["href"] = href.replace(hn_base, proxy_url)


def _rewrite_forms(
    soup: BeautifulSoup, proxy_url: str, hn_base: str
) -> None:
    """Заменяет action в формах на URL прокси."""
    for form in soup.find_all("form", action=True):
        action = form["action"]
        if action.startswith("/"):
            form["action"] = f"{proxy_url}{action}"
        elif _is_hn_url(action, hn_base):
            form["action"] = action.replace(hn_base, proxy_url)


def process_html(html: str, proxy_url: str) -> str:
    """
    Парсит HTML, модифицирует текст (™), ссылки и формы, возвращает HTML-строку.
    Пустая или пробельная строка возвращается без изменений. Парсер: lxml.
    """
    if not html or not html.strip():
        return html
    hn_base = settings.hn_base_url.rstrip("/")
    soup = BeautifulSoup(html, "lxml")
    _add_trademark_to_text_nodes(soup)
    _rewrite_links(soup, proxy_url, hn_base)
    _rewrite_forms(soup, proxy_url, hn_base)
    return str(soup)
