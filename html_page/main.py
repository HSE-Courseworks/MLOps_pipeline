import requests
import markdown
import os
from bs4 import BeautifulSoup
    
def md_to_html(github_readme_url):
    response = requests.get(github_readme_url)
    markdown_text = response.text
    html_documentation = markdown.markdown(markdown_text)
    return html_documentation

def update_html(github_readme_url):
    documentation = md_to_html(github_readme_url)

    with open('index.html', 'r', encoding='utf-8') as file:
        content = file.read()
        file.close()
    
    soup = BeautifulSoup(content, 'html.parser')    

    target_div = soup.find('div', id='docsSection')
    target_div.clear()

    add_soup = BeautifulSoup(documentation, 'html.parser')

    target_div.append(add_soup)
    
    if target_div.contents:
        target_div.contents[0].extract()

    prettified_html = soup.prettify(formatter='html5lib')

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(str(prettified_html))

    

def main():
    github_readme_url = 'https://raw.githubusercontent.com/HSE-Courseworks/MLOps_pipeline/main/README.md'

    update_html(github_readme_url)

if __name__ == "__main__":
    main()