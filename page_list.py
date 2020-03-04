from generating_pages import generate_easy_page, generate_hard_task, generate_easy_task
from pages import Page

# Create an empty list to store pages

# The pattern to create test
# 1 means easy
# 2 means difficult
PATTERN = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]


# Create a PAGES list for test page.
PAGES = []


def create_page(pattern):
    for i in pattern:
        if i == 1:
            x = generate_easy_page()
            for page in x:
                PAGES.append(page)
        elif i == 2:
            x = generate_hard_task()
            for page in x:
                PAGES.append(page)


create_page(PATTERN)
