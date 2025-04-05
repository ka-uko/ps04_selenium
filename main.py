import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def choose_article_from_search(browser):
    try:
        content_div = browser.find_element(By.ID, "content")  # Ищем основной контейнер
        search_results = content_div.find_elements(By.CSS_SELECTOR, "ul.mw-search-results li a")

        if not search_results:
            print("Нет результатов поиска на этой странице.")
            return False

        # Оставляем только первые 5 ссылок с нормальными названиями
        articles = []
        for link in search_results:
            title = link.get_attribute('data-prefixedtext')
            if title:  # Отбираем только те, у кого реально есть нормальное название
                articles.append((title, link))
            if len(articles) >= 5:
                break

        if not articles:
            print("Не удалось найти подходящие статьи.")
            return False

        print("\nДоступные статьи:")
        for idx, (title, _) in enumerate(articles, start=1):
            print(f"{idx}. {title}")

        while True:
            choice = input("\nВведите номер статьи для перехода или 'q' для возврата в меню: ")

            if choice.lower() == 'q':
                return False
            elif choice.isdigit() and 1 <= int(choice) <= len(articles):
                _, selected_link = articles[int(choice) - 1]
                href = selected_link.get_attribute('href')
                browser.get(href)
                time.sleep(2)
                return True
            else:
                print(f"Пожалуйста, введите число от 1 до {len(articles)} или 'q'.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False

def list_paragraphs(browser):
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    paragraphs = [p.text.strip() for p in paragraphs if p.text.strip()]  # Только непустые параграфы

    if not paragraphs:
        print("Параграфы на этой странице не найдены.")
        return

    current_title = browser.title.split(" —")[0]
    print(f"\nЧтение статьи: {current_title}")

    for i, paragraph in enumerate(paragraphs):
        print(f"\nПараграф {i + 1}:\n{paragraph}\n")
        next_action = input("Нажмите Enter для следующего параграфа или введите 'q' для выхода к меню: ")
        if next_action.lower() == 'q':
            break


def browse_internal_links(browser):
    hatnotes = []
    # Ищем все div-элементы на странице


    for element in browser.find_elements(By.TAG_NAME, "div"):
        try:
            cl = element.get_attribute("class")
            if cl == "hatnote navigation-not-searchable ts-main":
                hatnotes.append(element)
        except:
            continue

    if not hatnotes:
        print("Не найдено связанных ссылок на этой странице.")
        return False

    print("\nНайдены связанные статьи:")
    for idx, hatnote in enumerate(hatnotes):
        try:
            link = hatnote.find_element(By.TAG_NAME, "a")
            link_text = link.text.strip()
            print(f"{idx + 1}. {link_text}")
        except:
            continue

    choice = input("\nВведите номер статьи для перехода или нажмите Enter для случайного перехода: ")

    if choice.isdigit() and 1 <= int(choice) <= len(hatnotes):
        selected_hatnote = hatnotes[int(choice) - 1]
    else:
        selected_hatnote = random.choice(hatnotes)

    try:
        link = selected_hatnote.find_element(By.TAG_NAME, "a")
        href = link.get_attribute("href")
        browser.get(href)
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Ошибка перехода по ссылке: {e}")
        return False

def main():
    initial_request = input('Введите ваш запрос для поиска информации: ')

    browser = webdriver.Chrome()
    browser.get("https://ru.wikipedia.org/wiki/Заглавная_страница")
    time.sleep(2)

    assert "Википедия" in browser.title
    search_box = browser.find_element(By.ID, "searchInput")
    time.sleep(1)
    search_box.send_keys(initial_request)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    while True:
        print("\nЧто вы хотите сделать дальше?")
        print("1. Выбрать статью из первых 5ти результатов поиска")
        print("2. Листать параграфы текущей статьи")
        print("3. Перейти на одну из связанных страниц")
        print("4. Выйти из программы")

        user_choice = input("Введите номер действия (1, 2, 3 или 4): ")

        if user_choice == '1':
            success = choose_article_from_search(browser)
            if not success:
                continue
        elif user_choice == '2':
            list_paragraphs(browser)
        elif user_choice == '3':
            success = browse_internal_links(browser)
            if success:
                while True:
                    print("\nВыберите действие на новой странице:")
                    print("1. Листать параграфы текущей статьи")
                    print("2. Перейти на другую связанную страницу")
                    print("3. Вернуться в основное меню")

                    sub_choice = input("Введите номер действия (1, 2 или 3): ")

                    if sub_choice == '1':
                        list_paragraphs(browser)
                    elif sub_choice == '2':
                        browse_internal_links(browser)
                    elif sub_choice == '3':
                        break
                    else:
                        print("Некорректный ввод. Попробуйте снова.")
        elif user_choice == '4':
            print("Выход из программы...")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")

    browser.quit()

if __name__ == "__main__":
    main()



