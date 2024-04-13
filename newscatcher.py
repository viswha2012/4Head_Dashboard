from requests_html import HTMLSession

session = HTMLSession()
url = "https://news.google.com/rss/search?q=Karnataka Crime"
r = session.get(url)

titles = []

for title in r.html.find('title'):
    titles.append(title.text)
    if len(titles) >= 10:
        break

titles = titles[1:]

print(titles)
