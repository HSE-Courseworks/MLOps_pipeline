import requests
import markdown
from bs4 import BeautifulSoup
import html5lib
from html5lib.serializer import HTMLSerializer
import os

def md_to_html(github_readme_url):
    response = requests.get(github_readme_url)
    markdown_text = response.text
    html_documentation = markdown.markdown(markdown_text)
    return html_documentation


def clear_div_contents(target_div):
    target_div.clear()

def add_airflow_header(soup, target_div):
    h1_tag = soup.new_tag('h1')
    h1_tag.string = 'Airflow'
    target_div.append(h1_tag)

def add_airflow_link_and_paragraph(soup, target_div):
    paragraph = soup.new_tag('p')
    paragraph.append('Follow this ')
    link = soup.new_tag('a', href='http://localhost:8080/home', target='_blank')
    link.append('link')
    paragraph.append(link)
    paragraph.append(' to open Airflow.')

    target_div.append(paragraph)

def add_files_list(soup, target_div, files_in_dags):
    available_dags_label = soup.new_tag('p')
    available_dags_label.string = 'Available DAGs:'
    target_div.append(available_dags_label)

    ul = soup.new_tag('ul')
    for file_name in files_in_dags:
        li = soup.new_tag('li')
        li.string = file_name[:-3]
        ul.append(li)

    target_div.append(ul)

def update_documentation(github_readme_url, content):
    documentation = '<h1>Documentation</h1>' + md_to_html(github_readme_url)
    return content.replace('<h1>Documentation</h1>', documentation)

def update_airflow(content, files_in_dags):
    soup = BeautifulSoup(content, 'html.parser')
    target_div = soup.find('div', id='airflowSection')

    clear_div_contents(target_div)
    add_airflow_header(soup, target_div)
    add_airflow_link_and_paragraph(soup, target_div)
    add_files_list(soup, target_div, files_in_dags)

    return soup.prettify(formatter='html5')

def update_html(github_readme_url):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    files_in_dags = os.listdir(os.path.join(os.path.dirname(current_directory), 'airflow', 'dags'))
    index_html_path = os.path.join(current_directory, 'index.html')

    with open(index_html_path, 'r', encoding='utf-8') as file:
        content = file.read()

    updated_documentation = update_documentation(github_readme_url, content)
    updated_html = update_airflow(updated_documentation, files_in_dags)

    with open(index_html_path, 'w', encoding='utf-8') as file:
        file.write(updated_html)

def main():
    github_readme_url = 'https://raw.githubusercontent.com/HSE-Courseworks/MLOps_pipeline/main/README.md'
    update_html(github_readme_url)

=======

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
