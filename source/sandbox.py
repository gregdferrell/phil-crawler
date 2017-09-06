### IMPORTS

from datetime import datetime
from bs4 import BeautifulSoup

import pytz
import random
import re
import requests


### FUNCTIONS

def list_play():
    """
    Lists
    :return:
    """
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    print(months[6:9])
    print(months[:6])


# list_play()

def tuple_play():
    """
    Tuples
    Uses:
        Keys in Set/Dict (because unmutable)
        Return multiple values from func
        Two or more values closely related
    :return:
    """
    AngkorWat = (13.4125, 103.866667)
    print(type(AngkorWat))
    dimensions = 52, 40, 100  # create a tuple without parenthesis
    length, width, height = dimensions  # tuple unpacking


# tuple_play()

def set_play():
    countries = ['Angola', 'Maldives', 'India', 'United States', 'India']
    country_set = set(countries)  # Create set from list


# set_play()

def dictionaries_play():
    elements = {'hydrogen': 1, 'helium': 2, 'carbon': 6}
    elements['lithium'] = 3
    print(elements['lithium'])


# dictionaries_play()

def fib(n):
    if n <= 2:
        return 1
    return fib(n - 2) + fib(n - 1)


# fib(7)

def tuple_key():
    elements = {'a': 1, 'b': 2, 'c': 3}
    elements['d'] = 4
    efghlist = ['ef', 'gh']
    efghtup = ('ef', 'gh')
    #    elements[efghlist] = 5 # TypeError: unhashable type: 'list'
    elements[efghtup] = 6
    print(elements)


# tuple_key()


def hours2days(hours):
    return hours // 24, hours % 24


# hours2days(90)

def print_list(l, numbered=False, bullet_character='-'):
    """Prints a list on multiple lines, with numbers or bullets

    Arguments:
    l: The list to print
    numbered: set to True to print a numbered list
    bullet_character: The symbol placed before each list element. This is
                      ignored if numbered is True.
    """
    for index, element in enumerate(l):
        if numbered:
            print("{}: {}".format(index + 1, element))
        else:
            print("{} {}".format(bullet_character, element))


def todo_list(new_task, base_list=['wake up']):
    base_list.append(new_task)
    return base_list


def file_play():
    # read
    f = open('resources/testfile.txt', 'r')
    file_data = f.read()
    f.close()
    print(file_data)

    # write (always creates new/overwrites existing)
    f = open('resources/newfile.txt', 'w')
    f.write('i\'m a brand new file!')
    f.close()

    f = open('resources/newfile.txt', 'r')
    file_data = f.read()
    f.close()
    print(file_data)

    # append
    f = open('resources/testfile.txt', 'a')
    f.write('another line!\n')
    f.close()

    # one char at a time
    # with open('resources/testfile.txt', 'r') as f:
    #     while True:
    #         c = f.read(1)
    #         if not c:
    #             break
    #         print(c)

    # one line at a time
    with open('resources/testfile.txt', 'r') as f:
        for line in f:
            print(line)


def create_cast_list(filename):
    cast_list = []
    with open(filename, 'r') as f:
        for line in f:
            cast_list.append(line.split(',')[0])
    return cast_list


def print_randoms():
    objs = {}
    for i in range(100):
        val = random.randint(1, 10)
        if val in objs:
            objs[val] += 1
        else:
            objs[val] = 0

    for i in range(1, 11):
        print("{}: {}".format(i, objs[i]))


# print_randoms()

def regex_test(string):
    pattern = '/wiki/\w*:\w*'
    return re.match(pattern, string)


# r = regex_test('/wiki/Help:something')


def date_time_pytz():
    utc = pytz.utc  # Coordinated Universal Time
    ist = pytz.timezone('Asia/Kolkata')  # Indian Standard Time

    now = datetime.now(tz=utc)  # current time in UTC
    ist_now = now.astimezone(ist)  # current time in IST

    print(now)
    print(ist_now)


# date_time_pytz()


def password_generator():
    word_list = []
    with open('../resources/password-generation-words.txt', 'r') as f:
        for line in f:
            word = line.strip().lower()
            if 3 < len(word) < 8:
                word_list.append(word)

    pw = ''
    for i in range(1, 4):
        pw += word_list[random.randint(1, len(word_list))]

    print(pw)

# password_generator()

def crawler(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    p_tags = soup.find(id='mw-content-text').find(class_='mw-parser-output').find_all('p', recursive=False)
    for p in p_tags:
        p_stripped_str = re.sub(r'\(<a.+a>\)', '', str(p))
        p_sub = BeautifulSoup(p_stripped_str, 'html.parser')

        anchors = p_sub.find_all('a')
        val = ''
        for anchor in anchors:
            if anchor['href'].startswith('/wiki') \
                    and not re.match('/wiki/\w*:\w*', anchor['href']):
                val = anchor['href']
                break
        if val:
            break

    print("HREF: " + val)


# url = 'https://en.wikipedia.org/wiki/Sport'
# crawler(url)


def paren_stripper(text):
    left_paren_count = 0
    right_paren_count = 0
    l_index = -1
    r_index = -1
    ignore = False
    for i, c in enumerate(text):
        # ignore text in anchor tags
        if c == '<' and text[i+1] == 'a':
            ignore = True
        elif c == '>' and text[i-1] == 'a':
            ignore = False
        if not ignore:
            if c == '(':
                left_paren_count += 1
                if l_index == -1:
                    l_index = i
            if c == ')':
                right_paren_count += 1
                if left_paren_count == right_paren_count:
                    r_index = i
                    break
    if l_index > -1 and r_index > -1:
        return text[:l_index] + paren_stripper(text[r_index+1:])
    else:
        return text

# text = 'abc(123(456))def'
# print('1: ' + paren_stripper(text) + ' --- should be \'abcdef\'')
# text = 'abcdef'
# print('2: ' + paren_stripper(text) + ' --- should be \'abcdef\'')
# text = '(123456)'
# print('3: ' + paren_stripper(text) + ' --- should be \'\'')
# text = 'abc(123)'
# print('4: ' + paren_stripper(text) + ' --- should be \'abc\'')
# text = '(abc'
# print('5: ' + paren_stripper(text) + ' --- should be \'(abc\'')
# text = 'abc)'
# print('6: ' + paren_stripper(text) + ' --- should be \'abc)\'')
# text = ')abc('
# print('7: ' + paren_stripper(text) + ' --- should be \')abc(\'')
# text = 'a((123))bc(456)def'
# print('8: ' + paren_stripper(text) + ' --- should be \'abcdef\'')
# text = 'abc (<a href="/wiki/British_English" title="British English">British English</a>) def'
# print('9: ' + paren_stripper(text) + ' --- should be \'abc  def\'')
# text = '<p>a contest for <a href="/wiki/Territory_(animal)">territory</a>, a niche, for scarce</p>'
# print('10: ' + paren_stripper(text) + ' --- should be \'<p>a contest for <a href="/wiki/Territory_(animal)">territory</a>, a niche, for scarce</p>\'')
# text = 'abc <a href="/wiki/Territory_(animal)">territory</a>'
# print('11: ' + paren_stripper(text) + ' --- should be \'abc <a href="/wiki/Territory_(animal)">territory</a>\'')
# text = '<a href="/wiki/Territory_(animal)">territory</a> def'
# print('12: ' + paren_stripper(text) + ' --- should be \'<a href="/wiki/Territory_(animal)">territory</a> def\'')

