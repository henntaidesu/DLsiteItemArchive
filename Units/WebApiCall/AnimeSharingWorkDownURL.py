import requests
from lxml import html


def GETASWorkDowmURL(URL):
    try:
        url = f"https://www.anime-sharing.com/threads/{URL}/"
        response = requests.get(url)
        html_data = response.text
        tree = html.fromstring(html_data)

        # 使用XPath选择器来获取包含特定class的span元素

        L1 = tree.xpath('//span[contains(@class, "bbcode-box-content")]')
        L2 = tree.xpath('//div[contains(@class, "bbWrapper")]')
        # L3 = tree.xpath('//span[contains(@class, "bbcode-box")]')
        List = [L1, L2]
        Flag = 0
        for i in List:
            span_elements = i
            Flag += 1
            if None in span_elements:
                continue
            if span_elements:
                for span in span_elements:
                    # 获取span元素的文本内容
                    span_text = span.text_content()
                    # 获取span元素内的所有a标签的href属性
                    a_elements = span.xpath(".//a")
                    href_list = [a.get("href") for a in a_elements]  # 从第二个a标签开始
                    # print("href内容:", href_list)
                    return Flag, href_list


    except Exception as e:
        print("ERR:GETASWorkDowmURL", str(e))




