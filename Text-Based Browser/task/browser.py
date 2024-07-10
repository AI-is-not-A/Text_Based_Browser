import os
import sys
import requests
from bs4 import BeautifulSoup
from colorama import Fore

tags_to_show = "p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "ul", "ol", "li"
tabs_list = []
actual_page = ""


def accept_one_argument():
    args = sys.argv
    dir_name = args[1]
    path = f"{os.getcwd()}\\{dir_name}"
    if not os.access(path, mode=os.F_OK):
        os.mkdir(path)
    os.chdir(path)


def delete_tab():
    if len(tabs_list) > 0:
        print(tabs_list.pop())


def append_https_left_in_url(url):
    if "https://" not in url:
        return f"https://{url}"
    else:
        return url


def get_filename(url):
    return url.split(".")[0].replace("https://", "")


def save_page_to_file(url, page_text):
    with open(os.getcwd() + f"\\{get_filename(url)}", "w") as file:
        file.write(page_text)


def append_actual_page():
    if actual_page != "":
        tabs_list.append(actual_page)


def get_human_readable_text(r):
    soup = BeautifulSoup(r.content, "html.parser")
    content = []
    tags_to_skip = 0
    for tag in soup.find_all():
        if tags_to_skip != 0:
            tags_to_skip -= 1
            continue
        if tag.name in tags_to_show:
            readable_text = tag.get_text().strip()
            if tag.name == "a":
                readable_text = f"{Fore.BLUE}{readable_text}{Fore.RESET}"

            for inner_tag in tag.find_all():
                tags_to_skip += 1
                if inner_tag.name == "a" and inner_tag.string is not None:
                    readable_text = readable_text.replace(inner_tag.string,
                                                          f"{Fore.BLUE}{inner_tag.string}{Fore.RESET}")
            content.append(readable_text)

    content = [x.strip() for x in content]
    content = [x for x in content if x]
    return "\n".join(content)


def start():
    global actual_page
    while True:
        user_input = input().strip().lower()
        if user_input == "exit":
            exit()
        elif user_input == "back":
            delete_tab()
        else:
            user_url = append_https_left_in_url(user_input)
            try:
                r = requests.get(user_url)
            except requests.exceptions.ConnectionError:
                print("Invalid Url")
                continue
            site_text = get_human_readable_text(r)
            print(site_text)
            save_page_to_file(user_url, site_text)
            append_actual_page()
            actual_page = site_text


def main():
    accept_one_argument()
    start()


if __name__ == "__main__":
    main()
