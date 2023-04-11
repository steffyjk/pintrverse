import urllib.parse
import re

from browser_history import get_history
import tldextract


def get_history_list(range_number):
    outputs = get_history()  # HERE GET_HISTORY IS THE FUNCTION FROM BROWSER_HISTORY WHICH GONNA FETCH HISTORY OF USER
    print("----> this is outputs", outputs)
    his = outputs.histories

    history_list = []
    print('--->', his)
    count = 0
    for _ in range(range_number-1):
        count -= 1
        try:
            history_list.append(his[count])
        except:
            pass
    return history_list


def extract_keywords(history_list):
    keyword_list = []
    for history in history_list:

        history = history[1]  # HERE INDEX 1 ACTUALLYgit practice for rebase something error TAKES URL FROM THE TUPLE OF DATE TIME & URL [ SEARCH ]
        url = history

        parsed_url = urllib.parse.urlparse(url)
        query_string = parsed_url.query
        params = urllib.parse.parse_qs(query_string)

        if 'q' in params:  # HERE Q PARAM IS FOR (IF USER SEARCH SOMETHING ON SEARCH ENGINE CASE )
            keywords = re.findall('\w+', params['q'][0])
            keyword_list.extend(iter(keywords))
        else:  # ELSE PART IS FOR IF USER VISITS ANY OFFICIAL WEBSITE SO WE HAVE TO STORE THE DOMAIN DETAIL
            extracted = tldextract.extract(url)
            keywords = f"{extracted.domain}"
            keyword_list.append(keywords)

    return keyword_list

# # ans = extract_keywords(get_history_list(5))
# # print(ans)
