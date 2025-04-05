import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def choose_article_from_search(browser):
    try:
        content_div = browser.find_element(By.ID, "content")
        search_results = content_div.find_elements(By.CSS_SELECTOR, "ul.mw-search-results li a")

        articles = []
        for link in search_results:
            title = link.get_attribute('data-prefixedtext')
            if title:
                articles.append((title, link))
            if len(articles) >= 5:
                break

        if not articles:
            print("Не найдено подходящих статей.")
            return False

        print("\nНайдены статьи:")
        for idx, (title, _) in enumerate(articles, start=1):
            print(f"{idx}. {title}")

        while True:
            choice = input("\nВведите номер статьи для перехода: ")
            if choice.isdigit() and 1 <= int(choice) <= len(articles):
                _, selected_link = articles[int(choice) - 1]
                href = selected_link.get_attribute('href')
                browser.get(href)
                time.sleep(2)
                return True
            else:
                print(f"Введите число от 1 до {len(articles)}.")

    except Exception as e:
        print(f"Ошибка при выборе статьи: {e}")
        return False

def list_paragraphs(browser):
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    paragraphs = [p.text.strip() for p in paragraphs if p.text.strip()]

    if not paragraphs:
        print("Параграфы не найдены.")
        return

    current_title = browser.title.split(" —")[0]
    print(f"\nЧтение статьи: {current_title}")

    for idx, paragraph in enumerate(paragraphs, 1):
        print(f"\nПараграф {idx}:\n{paragraph}\n")
        if input("Нажмите Enter для следующего параграфа или 'q' для выхода: ").lower() == 'q':
            break

def browse_internal_links(browser):
    hatnotes = []
    for element in browser.find_elements(By.TAG_NAME, "div"):
        try:
            if element.get_attribute("class") == "hatnote navigation-not-searchable ts-main":
                hatnotes.append(element)
        except:
            continue

    if not hatnotes:
        print("Связанные страницы не найдены.")
        return False

    print("\nСвязанные статьи:")
    links = []
    for hatnote in hatnotes:
        try:
            link = hatnote.find_element(By.TAG_NAME, "a")
            links.append(link)
            print(f"{len(links)}. {link.text.strip()}")
        except:
            continue

    choice = input("\nВведите номер статьи для перехода или Enter для случайного выбора: ")
    if choice.isdigit() and 1 <= int(choice) <= len(links):
        link = links[int(choice) - 1]
    else:
        link = random.choice(links)

    try:
        href = link.get_attribute('href')
        browser.get(href)
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Ошибка перехода: {e}")
        return False

def after_article_menu(browser):
    while True:
        print("\nЧто хотите сделать?")
        print("1. Листать параграфы статьи")
        print("2. Перейти на связанную страницу")
        print("3. Выйти из программы")

        choice = input("Введите номер действия: ")

        if choice == '1':
            list_paragraphs(browser)
        elif choice == '2':
            if browse_internal_links(browser):
                continue  # После перехода снова показываем меню
            else:
                print("Не удалось перейти, остаемся на текущей странице.")
        elif choice == '3':
            print("Выход из программы...")
            return
        else:
            print("Некорректный ввод. Попробуйте снова.")

def main():
    initial_request = input('Введите ваш запрос для поиска информации: ')

    browser = webdriver.Chrome()
    try:
        browser.get("https://ru.wikipedia.org/wiki/Заглавная_страница")
        time.sleep(2)

        assert "Википедия" in browser.title
        search_box = browser.find_element(By.ID, "searchInput")
        search_box.send_keys(initial_request)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        if choose_article_from_search(browser):
            after_article_menu(browser)
        else:
            print("Не удалось выбрать статью. Завершаем программу.")

    finally:
        browser.quit()

if __name__ == "__main__":
    main()
