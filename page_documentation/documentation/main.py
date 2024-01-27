import requests
import markdown
        
def saveReadme(github_readme_url):
    response = requests.get(github_readme_url)

    if response.status_code == 200:
        with open('readme.md', 'w', encoding='utf-8') as file:
            file.write(response.text)
            print("Файл успешно сохранен")
    else:
        print("Запрос завершился неудачей. Код состояния:", response.status_code)
    file.close()

def md_to_html(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        markdown_text = file.read()

    html = markdown.markdown(markdown_text)

    with open('documentation.html', 'w', encoding='utf-8') as file:
        file.write(html)

def main():
    github_readme_url = 'https://raw.githubusercontent.com/HSE-Courseworks/MLOps_pipeline/main/README.md'

    saveReadme(github_readme_url)

    md_to_html('readme.md')


if __name__ == "__main__":
    main()
