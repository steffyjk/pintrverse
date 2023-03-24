import urllib.parse
import re

from browser_history import get_history
import tldextract


def get_history_list(range_number):
    outputs = get_history()
    his = outputs.histories

    history_list = []
    count = 0
    for _ in range(range_number):
        count -= 1
        history_list.append(his[count])
    return history_list


def extract_keywords(history_list):
    keyword_list = []
    for history in history_list:
        history = history[1]
        url = history

        parsed_url = urllib.parse.urlparse(url)
        query_string = parsed_url.query
        params = urllib.parse.parse_qs(query_string)

        if 'q' in params:
            keywords = re.findall('\w+', params['q'][0])
            keyword_list.extend(iter(keywords))
        else:
            extracted = tldextract.extract(url)
            keywords = f"{extracted.domain}"
            keyword_list.append(keywords)
    return list(set(keyword_list))


ans = extract_keywords(get_history_list(5))
print(ans)
