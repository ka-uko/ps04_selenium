#import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver import Keys
#
# initial_request = input('Введите ваш запрос для поиска информации: ')
#
# browser = webdriver.Chrome()
# browser.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
# time.sleep(3)
#
#
#
# assert "Википедия" in browser.title
# search_box = browser.find_element(By.ID, "searchInput")
# time.sleep(3)
# search_box.send_keys(initial_request)
# search_box.send_keys(Keys.RETURN)
# time.sleep(5)
# browser.quit()

# def choose_article_from_search(browser):
#     search_results = browser.find_elements(By.CSS_SELECTOR, "ul.mw-search-results li a")
#
#     if not search_results:
#         print("Нет результатов поиска на этой странице.")
#         return False
#
#     # Берем только первые 5 результатов (если их меньше, берем сколько есть)
#     search_results = search_results[:5]
#
#     print("\nДоступные статьи:")
#     for idx, link in enumerate(search_results, start=1):
#         title = link.get_attribute('data-prefixedtext')  # Берем красивое название из атрибута
#         if not title:  # Если по какой-то причине атрибута нет — берем текст ссылки
#             title = link.text
#         print(f"{idx}. {title}")
#
#     while True:
#         choice = input("\nВведите номер статьи для перехода или 'q' для возврата в меню: ")
#
#         if choice.lower() == 'q':
#             return False
#         elif choice.isdigit() and 1 <= int(choice) <= len(search_results):
#             selected_link = search_results[int(choice) - 1]
#             href = selected_link.get_attribute('href')
#             browser.get(href)
#             time.sleep(2)
#             return True
#         else:
#             print(f"Пожалуйста, введите число от 1 до {len(search_results)} или 'q'.")

#
#
#
# def browse_internal_links(browser):
#     hatnotes = []
#     # Ищем все div-элементы на странице
#     for element in browser.find_elements(By.TAG_NAME, "div"):
#         cl = element.get_attribute("class")
#         if cl == "hatnote navigation-not-searchable ts-main":
#             hatnotes.append(element)
#
#     print(hatnotes)
#
#     if not hatnotes:
#         print("Нет связанных статей на этой странице.")
#         return False
#
#     # Выбираем случайный элемент
#     hatnote = random.choice(hatnotes)
#
#     # Ищем ссылку внутри выбранного div
#     link = hatnote.find_element(By.TAG_NAME, "a").get_attribute("href")
#
#     # Переходим по найденной ссылке
#     browser.get(link)
#     time.sleep(2)
#     return True

# def random_article_from_search(browser):
#     search_results = browser.find_elements(By.CSS_SELECTOR, "ul.mw-search-results li a")
#
#     if not search_results:
#         print("Нет результатов поиска на этой странице.")
#         return False
#
#     while True:
#         random_link = random.choice(search_results)
#         title = random_link.text
#         href = random_link.get_attribute('href')
#
#         print(f"\nНайдена статья: {title}")
#         action = input("Нажмите Enter для перехода на статью или 'q' для возврата в меню: ")
#         if action.lower() == 'q':
#             return False
#         else:
#             browser.get(href)
#             time.sleep(2)
#             return True