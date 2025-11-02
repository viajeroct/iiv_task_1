import requests
from bs4 import BeautifulSoup


def make_google_request(start, lang, text):
    params = '+'.join(text.split(' '))
    print(f'Making request to google scholar, start={start}, params={params}')
    url = f"https://scholar.google.com/scholar?start={start}&q={params}&hl={lang}"
    headers = {
        'Cookie': '__cf_bm=QgYlUJ82T1dRY9BYQ293dA5zbXQX9gNRyc2vxthpSmg-1762069113-1.0.1.1-B_ceCOMqTp8RHYtsDfznzSBtbkg0XT26pf5oh0DeR2mJq.CeTI1Jsl90UDaaTDlh7m8ZLF.LxPb3xG6wHony__b4Jd6Z4NutYKdSIxjA_mE',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        print(f"Status Code: {response.status_code}")
        print("=" * 50)

        if response.status_code == 200:
            return response.text
        else:
            print(f"Ошибка: Сервер вернул статус {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")


def extract_article_titles(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    titles = []

    title_elements = soup.find_all('h3', class_='gs_rt')

    for title_element in title_elements:
        for span in title_element.find_all('span', class_='gs_ctc'):
            span.decompose()

        link = title_element.find('a')
        if link:
            title_text = link.get_text().strip()
            if title_text:
                titles.append(title_text)

    return titles


if __name__ == "__main__":
    pages = 10
    lang="en" # or ru
    for k in range(pages):
        content = make_google_request(k * 10, lang, "asynchronous programming in kotlin in web")
        result = extract_article_titles(content)

        print(f"Найдено {len(result)} статей:")
        for i, title in enumerate(result, 1):
            print(f"{i}. {title}")
        print("=" * 50)
