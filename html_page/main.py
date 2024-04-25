import markdown
import os


def find_tags(section_id):
    with open(index_html_path, "r", encoding="utf-8") as file:
        html_page = file.read()

    start_tag = f'<div class="section" id="{section_id}">'
    current_tag = "div"
    start_position = html_page.find(start_tag)
    stack = [start_position + 1]
    current_position = start_position + 1

    while True:
        current_position = html_page.find(current_tag, current_position + 1)
        if html_page[current_position - 2 : current_position + 4] == "</div>":
            stack.pop()
        elif html_page[current_position - 1 : current_position + 3] == "<div":
            stack.append(current_position)

        if len(stack) == 0:
            end_position = current_position - 2
            break

    return start_tag, start_position, end_position


def make_documentation():
    make_launching()
    make_description()
    make_tg_api()
    make_tg_script()
    make_db()


def make_launching():
    with open(index_html_path, "r", encoding="utf-8") as file:
        html_page = file.read()

    with open(launching_path, "r", encoding="utf-8") as file:
        markdown_text = file.read()

    html_content = markdown.markdown(markdown_text)

    start_tag, start_position, end_position = find_tags("projectLaunching")

    updated_html_content = (
        html_page[: start_position + len(start_tag)]
        + back_button
        + html_content
        + html_page[end_position:]
    )
    write_to_index(updated_html_content)


def make_description():
    with open(index_html_path, "r", encoding="utf-8") as file:
        html_page = file.read()

    with open(description_path, "r", encoding="utf-8") as file:
        markdown_text = file.read()

    html_content = markdown.markdown(markdown_text)
    start_tag, start_position, end_position = find_tags("projectDescription")

    updated_html_content = (
        html_page[: start_position + len(start_tag)]
        + back_button
        + html_content
        + html_page[end_position:]
    )
    write_to_index(updated_html_content)


def make_tg_api():
    with open(index_html_path, "r", encoding="utf-8") as file:
        html_page = file.read()

    with open(tg_api_path, "r", encoding="utf-8") as file:
        markdown_text = file.read()

    html_content = markdown.markdown(markdown_text)

    start_tag, start_position, end_position = find_tags("tgAPI")

    updated_html_content = (
        html_page[: start_position + len(start_tag)]
        + back_button
        + html_content
        + html_page[end_position:]
    )
    write_to_index(updated_html_content)


def make_tg_script():
    with open(index_html_path, "r", encoding="utf-8") as file:
        html_page = file.read()
    with open(tg_script_path, "r", encoding="utf-8") as file:
        markdown_text = file.read()

    html_content = markdown.markdown(markdown_text)

    start_tag, start_position, end_position = find_tags("tgScript")

    updated_html_content = (
        html_page[: start_position + len(start_tag)]
        + back_button
        + html_content
        + html_page[end_position:]
    )
    write_to_index(updated_html_content)


def make_db():
    with open(index_html_path, "r", encoding="utf-8") as file:
        html_page = file.read()
    with open(databases_md_path, "r", encoding="utf-8") as file:
        markdown_text = file.read()

    html_content = markdown.markdown(markdown_text)

    start_tag, start_position, end_position = find_tags("db")

    updated_html_content = (
        html_page[: start_position + len(start_tag)]
        + back_button
        + html_content
        + html_page[end_position:]
    )
    write_to_index(updated_html_content)


def write_to_index(content):
    with open(index_html_path, "w", encoding="utf-8") as file:
        file.write(content)


back_button = (
    """<span class="back-to-docs" onclick="showSection('docsSection')"></span>"""
)

current_directory = os.getcwd()

index_html_path = os.path.join(current_directory, "html_page", "index.html")
databases_md_path = os.path.join(current_directory, "documentation", "DATABASES.md")
tg_script_path = os.path.join(current_directory, "documentation", "TELEGRAMSCRIPT.md")
tg_api_path = os.path.join(current_directory, "documentation", "TELEGRAMAPI.md")
launching_path = os.path.join(current_directory, "documentation", "PROJECTLAUNCHING.md")
description_path = os.path.join(
    current_directory, "documentation", "PROJECTDESCRIPTION.md"
)

if __name__ == "__main__":
    make_documentation()
