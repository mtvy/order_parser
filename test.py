import parsing

page = f"{parsing.DEFAULT_LINK}/{parsing.MAIN_PREF}"

def test_browser():
    parsing.imit_browser(page)
    
if __name__ == "__main__":
    # test_parsing()
    test_browser()