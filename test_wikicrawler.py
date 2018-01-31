from wikicrawler import crawl_wikipedia_path_to_philosophy, \
    SEARCH_DONE_FOUND_PHILOSOPHY, SEARCH_DONE_INFINITE_LOOP, \
    SEARCH_DONE_MAX_COUNT


def test_crawl_finds_philosophy():
    # Test Description: End state: Finds Philosophy

    url = 'https://en.wikipedia.org/wiki/Ethology'
    articles_visited, result_string = crawl_wikipedia_path_to_philosophy(url)
    assert articles_visited[0] == url
    assert articles_visited[-1] == 'https://en.wikipedia.org/wiki/Philosophy'
    assert result_string == SEARCH_DONE_FOUND_PHILOSOPHY


def test_crawl_infinite_loop():
    # Test Description: End state: Infinite loop
    # (Mathematics->Quantity->Counting->Finite_set->Mathematics)

    url = 'https://en.wikipedia.org/wiki/Mathematics'
    articles_visited, result_string = crawl_wikipedia_path_to_philosophy(url)
    assert articles_visited[0] == url
    assert articles_visited[-1] == url
    assert result_string == SEARCH_DONE_INFINITE_LOOP


def test_crawl_max_out():
    # Test Description: End state: Reaches max count

    max_pages = 3
    url = 'https://en.wikipedia.org/wiki/Throne'
    articles_visited, result_string = \
        crawl_wikipedia_path_to_philosophy(url, max_pages)
    assert articles_visited[0] == url
    assert len(articles_visited) == max_pages
    assert result_string == SEARCH_DONE_MAX_COUNT
