import csv
import copy
import random
from pages import Page

page_list = []


with open("word_list.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_counter = 0
    for row in csv_reader:
        if line_counter == 0:
            line_counter += 1
            continue
        else:
            page_list.append(Page(chinese=row[0], answer=row[1], hint=row[2]))


def generate_easy_task():
    sample_dict = {}
    ran_num_1 = random.randint(1, len(page_list) - 1)
    ran_num_2 = random.randint(1, len(page_list) - 1)
    page_1 = page_list.pop(ran_num_1)
    page_2 = page_list.pop(ran_num_2)
    sample_dict[0] = page_1
    sample_dict[1] = page_2
    return sample_dict


def generate_easy_page():
    sample_dict = generate_easy_task()
    displaying_page = []
    for i in range(10):
        PAGE_1 = sample_dict[0]
        PAGE_2 = sample_dict[1]
        if i == 0:
            displaying_page.append(PAGE_1)
        elif i == 1:
            displaying_page.append(PAGE_2)
        elif i > 1:
            if i % 2 == 0:
                PAGE_3 = copy.copy(PAGE_1)
                PAGE_3.set_hint_off()
                displaying_page.append(PAGE_3)
            elif i % 2 != 0:
                if i == 9:
                    x = copy.copy(PAGE_2)
                    x.set_survey(1)
                    x.set_hint_off()
                    displaying_page.append(x)
                else:
                    PAGE_4 = copy.copy(PAGE_2)
                    PAGE_4.set_hint_off()
                    displaying_page.append(PAGE_4)
    return displaying_page


def generate_hard_task():
    PAGE = []
    page_1 = page_list.pop()
    page_2 = page_list.pop()
    page_3 = page_list.pop()

    page_1_clone = copy.copy(page_1)
    page_1_clone.set_hint_off()

    page_2_clone = copy.copy(page_2)
    page_2_clone.set_hint_off()

    page_3_clone = copy.copy(page_3)
    page_3_clone.set_hint_off()

    page_4 = copy.copy(page_1)
    page_4.join_chinese(page_2)
    page_4.set_hint_off()

    page_5 = copy.copy(page_2)
    page_5.join_chinese(page_1)
    page_5.set_hint_off()

    page_6 = copy.copy(page_3)
    page_6.join_chinese(page_1)
    page_6.set_hint_off()

    page_7 = copy.copy(page_3)
    page_7.join_chinese(page_2)
    page_7.set_hint_off()

    page_8 = copy.copy(page_3)
    page_8.join_chinese(page_2)
    page_8.join_chinese(page_1)
    page_8.set_hint_off()

    page_9 = copy.copy(page_1)
    page_9.join_chinese(page_2)
    page_9.join_chinese(page_3)
    page_9.set_hint_off()

    page_10 = copy.copy(page_2)
    page_10.join_chinese(page_1)
    page_10.join_chinese(page_3)
    page_10.set_hint_off()

    page_10.set_survey(2)

    for i in range(13):
        if i == 0:
            PAGE.append(page_1)
        elif i == 1:
            PAGE.append(page_1_clone)
        elif i == 2:
            PAGE.append(page_2)
        elif i == 3:
            PAGE.append(page_2_clone)
        elif i == 4:
            PAGE.append(page_4)
        elif i == 5:
            PAGE.append(page_5)
        elif i == 6:
            PAGE.append(page_3)
        elif i == 7:
            PAGE.append(page_3_clone)
        elif i == 8:
            PAGE.append(page_6)
        elif i == 9:
            PAGE.append(page_7)
        elif i == 10:
            PAGE.append(page_8)
        elif i == 11:
            PAGE.append(page_9)
        elif i == 12:
            PAGE.append(page_10)
    return PAGE
