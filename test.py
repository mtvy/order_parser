import parsing, requests

from logger import log

page = f"{parsing.DEFAULT_LINK}/{parsing.MAIN_PREF}"

def test_parsing():
    log.info(page)
    parsing.parse(page)
    r = requests.post(page, params={"did":123, "ng":456})
    print(r.text)

def test_browser():
    parsing.imit_browser(page)
    
if __name__ == "__main__":
    # test_parsing()
    test_browser()