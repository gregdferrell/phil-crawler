from bs4 import BeautifulSoup
import re
import requests
from time import sleep


def crawl_wikipedia_path_to_philosophy(starting_url, max_links=20):
    """
    Get the path to the Philosophy wiki page following the first link in the main
    body of the given url.
    :param starting_url: the starting wikipedia page
    :param max_links: the maximum number of links to search
    :return: a list of URL strings from the first page to the last
    """

    articles_visited = []
    get_url = starting_url

    while continue_with_search(articles_visited, get_url, max_links):
        response = requests.get(get_url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # Add article to list
        articles_visited.append(get_url)

        # Find next url
        get_url = extract_next_wiki_link(soup)

        # Don't want to hit wikipedia server too hard
        sleep(1)


def continue_with_search(articles_visited, get_url, max_links):
    # Check if reached max count
    if len(articles_visited) == max_links:
        print('I traveled a great distance, then got really tired and quit')
        return False

    print('Step ' + str(len(articles_visited) + 1) + ': ' + get_url)

    # Check for philosophy page
    if get_url == 'https://en.wikipedia.org/wiki/Philosophy':
        print('I traveled a great distance, and found philosophy')
        return False

    # Check if page has already been encountered
    if get_url in articles_visited[:-1]:
        print('I traveled a great distance, only to find myself in an infinite loop')
        return False

    # Check if the page has no valid link
    if not get_url:
        print('I traveled a great distance, but ran into a dead end from which I cannot return')
        return False

    return True


def extract_next_wiki_link(soup):
    """
    Given the soup of a wikipedia page, return the href of the next link from the main
    body or empty string if none is found.
    :param soup: a soup of a wikipedia page
    :return: a string representing an href to the next wikipedia page or null if none found
    """

    p_tags = soup.find(id='mw-content-text').find(class_='mw-parser-output').find_all('p', recursive=False)
    for p in p_tags:
        p_stripped_str = strip_out_parenthesis(str(p))
        p_sub = BeautifulSoup(p_stripped_str, 'html.parser')

        anchors = p_sub.find_all('a')
        for anchor in anchors:
            if anchor['href'].startswith('/wiki') \
                    and not re.match('/wiki/\w*:\w*', anchor['href']):
                return 'https://en.wikipedia.org' + anchor['href']


def strip_out_parenthesis(text):
    """
    Strips out text enclosed by parenthesis (including the parenthesis). Does not strip
    out text if the parenthesis are within an anchor tag -this is because some valid
    anchor tags for this application have parenthesis in the href.
    :param text: the text to strip the parenthesis from
    :return: the remaining text
    """

    left_paren_count = 0
    right_paren_count = 0
    l_index = -1
    r_index = -1
    ignore = False
    for i, c in enumerate(text):
        # don't remove text within anchor tags
        if c == '<' and text[i + 1] == 'a':
            ignore = True
        elif c == '>' and text[i - 1] == 'a':
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
        return text[:l_index] + strip_out_parenthesis(text[r_index + 1:])
    else:
        return text


if __name__ == '__main__':

    # Test 1: End state: Finds Philosophy
    # Tests:
    #   1. Skipping links in parenthesis that we don't want to follow (on page: Sport)
    #   2. Not skipping links that have parenthesis in them (on page: Objectivity (philosophy))
    #
    # url = 'https://en.wikipedia.org/wiki/Sport'
    # get_wikipedia_path_to_philosophy(url)

    # Test 2: End state: Infinite loop (Mathematics->Quantity->Counting->Finite_set->Mathematics)
    #
    # url = 'https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol'
    # get_wikipedia_path_to_philosophy(url)

    # Test 3: End state: Reaches max count
    # Tests:
    #   1. Only follow /wiki/* hyperlinks (on page: Potentate)
    #
    # url = 'https://en.wikipedia.org/wiki/Throne'
    # get_wikipedia_path_to_philosophy(url, 10)

    url = 'https://en.wikipedia.org/wiki/Special:Random'
    crawl_wikipedia_path_to_philosophy(url)
