from bs4 import BeautifulSoup
import re
import requests
from time import sleep

SEARCH_DONE_STUCK = 'I traveled a great distance, but ran into a dead end from which I cannot return'

SEARCH_DONE_INFINITE_LOOP = 'I traveled a great distance, only to find myself in an infinite loop'

SEARCH_DONE_FOUND_PHILOSOPHY = 'I traveled a great distance, and found philosophy'

SEARCH_DONE_MAX_COUNT = 'I traveled a great distance, then got really tired and quit'

CONTINUE_SEARCH = 'Continue search'


def crawl_wikipedia_path_to_philosophy(starting_url, max_links=20):
    """
    Get the path to the Philosophy wiki page following the first link in the main
    body of the given url.
    :param starting_url: the starting wikipedia page
    :param max_links: the maximum number of links to search
    :return: a tuple containing (0) a list of URL strings from the first page to the last and (1) a search result string
    """

    articles_visited = []
    get_url = starting_url

    result = True
    while result:
        print('Step ' + str(len(articles_visited) + 1) + ': ' + get_url)

        response = requests.get(get_url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # Add article to list
        articles_visited.append(get_url)

        # Find next url
        get_url = extract_next_wiki_link(soup)

        # Determine whether or not to continue
        result, result_description = continue_with_search(articles_visited, get_url, max_links)

        # If we are continuing, sleep so we don't hit the wikipedia server too hard
        if result:
            sleep(1)

    return articles_visited, result_description


def continue_with_search(articles_visited, next_url, max_links):
    '''
    Determines whether or not to continue with the search.
    :param articles_visited: the list of articles visited until now
    :param next_url: the next url to visit
    :param max_links: the max number of pages allowed to visit
    :return: a tuple containing (0) a boolean indicating whether or not to continue the search and (1) a reason
    '''

    # Check if reached max count
    if len(articles_visited) == max_links:
        return False, SEARCH_DONE_MAX_COUNT

    # Check for philosophy page
    if articles_visited[-1] == 'https://en.wikipedia.org/wiki/Philosophy':
        return False, SEARCH_DONE_FOUND_PHILOSOPHY

    # Check if page has already been encountered
    if articles_visited[-1] in articles_visited[:-1]:
        return False, SEARCH_DONE_INFINITE_LOOP

    # Check if the page has no valid link
    if not next_url:
        return False, SEARCH_DONE_STUCK

    return True, CONTINUE_SEARCH


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
    url = 'https://en.wikipedia.org/wiki/Special:Random'
    print(crawl_wikipedia_path_to_philosophy(url))
