import requests
import markdown
from bs4 import BeautifulSoup
import html5lib
from html5lib.serializer import HTMLSerializer


def md_to_html(github_readme_url):
    response = requests.get(github_readme_url)
    markdown_text = response.text
    html_documentation = markdown.markdown(markdown_text)
    return html_documentation


def update_html(github_readme_url):
    documentation = "<h1>Documentation</h1>" + md_to_html(github_readme_url)

    with open("index.html", "r", encoding="utf-8") as file:
        content = file.read()

    soup = BeautifulSoup(content, "html.parser")

    target_div = soup.find("div", id="docsSection")
    target_div.clear()

    add_soup = BeautifulSoup(documentation, "html.parser")

    target_div.append(add_soup)

    if target_div.contents:
        target_div.contents[1].extract()

    prettified_html = soup.prettify(formatter="html5")

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(prettified_html)


def main():
    github_readme_url = "https://raw.githubusercontent.com/HSE-Courseworks/MLOps_pipeline/main/README.md"

    update_html(github_readme_url)


if __name__ == "__main__":
    main()
