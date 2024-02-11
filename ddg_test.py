import threading
from duckduckgo_search import DDGS

def do_Search():
    with DDGS() as ddgs:
        searchResults = [r for r in ddgs.text('What is duckduckgo?', max_results=5)]
        print(searchResults)

def main():
    x = threading.Thread(target=do_Search)
    x.start()
    x.join()
    #do_Search()

if __name__ == '__main__':
    main()