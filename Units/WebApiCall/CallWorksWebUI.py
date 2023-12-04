import requests
from bs4 import BeautifulSoup
import re
import datetime
from datetime import datetime
import sys
import gc
import bs4
from Units.NowTime import NowTime

def TrimString(Str):
    if '\n' in Str:
        Str = Str.replace('\n', ' ')
    if ' ' in Str:
        Str = Str.replace(' ', '')
    if '/' in Str:
        Str = Str.replace('/', ' ')
    if "'" in Str:
        Str = Str.replace("'", "\\'")
    if '"' in Str:
        Str = Str.replace('"', '\\"')
    return Str


def CallWorksWebUI(work_id, work_type):
    # print(work_id, work_type)
    # work_id = "RJ005113"
    try:
        gc.collect()
        tag = None
        release_data = None
        update_data = None
        age_specification = None
        work_format = None
        file_format = None
        event = None
        capacity = None
        voice_actor = None
        scenario = None
        author = None
        series = None
        page_number = None
        languages = None
        music = None
        action_environment = None
        illustration = None
        others = None
        coupling = None
        img_path = None
        IntroductionForfWorks = None
        WorkDetails = None
        IfRelease = False

        Url1 = f"https://www.dlsite.com/maniax/work/=/product_id/{work_id}.html"
        Url2 = f"https://www.dlsite.com/maniax/announce/=/product_id/{work_id}.html"
        TagApi = f"https://www.dlsite.com/maniax/api/review?product_id={work_id}&limit=1&mix_pickup=true&locale=ja_JP"
        html1 = requests.get(Url1)
        try:
            WebData = BeautifulSoup(html1.text, 'html.parser')
            # 生成Tag
            TagDiv = WebData.find('div', class_="main_genre")
            li_elements = TagDiv.find_all('a')
            TagList = []
            if li_elements:
                for li in li_elements:
                    tag = li.text
                    if "/" in tag:
                        tag = tag.replace("/", " ")
                    TagList.append(tag)
                tag = " ".join(TagList)
            # WebDataSrt = WebData
            # WebDataSrt = str(WebDataSrt)
            # WebDataSrt = HtmlTrim(WebDataSrt)
            # sql = f"INSERT INTO `DLsite`.`html_text`(`rj_number`, `html_text`, `text_state`, `html_from`) " \
            #       f"VALUES ('{work_id}', '{WebDataSrt}', '0', '2');"
            # InsertALL(sql)
            # print(f"{work_id}:已写入原始HtmlText,数据来源DL")


        except Exception as e:
            try:
                html2 = requests.get(Url2)
                html1 = html2
                WebData = BeautifulSoup(html1.text, 'html.parser')
                # 生成Tag
                TagDiv = WebData.find('div', class_="main_genre")
                li_elements = TagDiv.find_all('a')
                TagList = []
                if li_elements:
                    for li in li_elements:
                        tag = li.text
                        if "/" in tag:
                            tag = tag.replace("/", " ")
                        TagList.append(tag)
                    tag = " ".join(TagList)
                    IfRelease = True
                # WebDataSrt = WebData
                # WebDataSrt = str(WebDataSrt)
                # WebDataSrt = HtmlTrim(WebDataSrt)
                # sql = f"INSERT INTO `DLsite`.`html_text`(`rj_number`, `html_text`, `text_state`, `html_from`) " \
                #       f"VALUES ('{work_id}', '{WebDataSrt}', '0', '2');"
                # InsertALL(sql)
                # print(f"{work_id}:已写入原始HtmlText,数据来源DL")

            except:
                return 10, "ERROR"

        # 查找详细信息
        table = WebData.find('table', id='work_outline')
        # 找到所有的<tr>元素
        tr_elements = table.find_all('tr')
        # 遍历每个<tr>元素，提取<td>元素中的数据
        for tr in tr_elements:
            th = tr.find('th')
            td = tr.find('td')

            if th:
                th = th.text.strip()

            if td:
                td = td.text.strip()

            if th == "販売日":
                release_data = td
                SrtLen = (len(release_data))
                if SrtLen > 11:
                    release_data = release_data[:11]
                release_data = release_data.replace("年", "-")
                release_data = release_data.replace("月", "-")
                release_data = release_data.replace("日", "")

            if th == "予告開始日":
                release_data = td
                SrtLen = (len(release_data))
                if SrtLen > 11:
                    release_data = release_data[:11]
                release_data = release_data.replace("年", "-")
                release_data = release_data.replace("月", "-")
                release_data = release_data.replace("日", "")

            if th == "ファイル容量":
                file_capacity = td
                if 'GB' in file_capacity:
                    match = re.search(r'(\d+\.\d+)', file_capacity)
                    if match:
                        capacity = float(match.group(1))
                if 'MB' in file_capacity:
                    match = re.search(r'(\d+\.\d+)', file_capacity)
                    if match:
                        file_capacity = float(match.group(1))
                        file_capacity = file_capacity / 1024
                        capacity = round(file_capacity, 3)

            if th == "年齢指定":
                age_specification = td
                age_specification = TrimString(age_specification)
                match age_specification:
                    case "全年齢":
                        age_specification = "1"
                    case "R-15":
                        age_specification = "2"
                    case "18禁":
                        age_specification = "3"

            if th == "作品形式":
                work_format = td
                work_format = TrimString(work_format)


            if th == 'ファイル形式':
                file_format = td
                file_format = TrimString(file_format)
                if len(file_format) > 64:
                    file_format = file_format[:64]

            if th == "イベント":
                event_label = WebData.find('th', text="イベント")
                if event_label:
                    event_span = event_label.find_next('td').find('span')
                    if event_span:
                        event = event_span.get('title')
                if len(event) > 64:
                    event = event[:64]

            if th == "声優":
                voice_actor = td
                voice_actor = TrimString(voice_actor)

            if th == "シナリオ":
                scenario = td
                scenario = TrimString(scenario)

            if th == "作者":
                author = td
                author = TrimString(author)
                if len(author) > 64:
                    author = author[:64]

            if th == "シリーズ名":
                series = td
                series = TrimString(series)
                if len(series) > 64:
                    series = series[:64]

            if th == "ページ数":
                page_number = td
                page_number = re.findall(r'\d+', page_number)
                page_number = (page_number[0])

            if th == '対応言語':
                languages = []
                language = WebData.find('th', text="対応言語")
                if language:
                    language_spans = language.find_next('td').find_all('span')
                    for language_span in language_spans:
                        title = language_span.get('title')
                        if title:
                            languages.append(title)
                languages = str(languages)
                if '[' in languages:
                    languages = languages.replace('[', '')
                if ']' in languages:
                    languages = languages.replace(']', '')
                if ',' in languages:
                    languages = languages.replace(',', '')
                if "'" in languages:
                    languages = languages.replace("'", "")

            if len(language) > 64:
                language = language[:64]

            if th == "音楽":
                music = td
                music = TrimString(music)
                if len(music) > 64:
                    music = music[:64]

            if th == "動作環境":
                action_environment = td
                action_environment = TrimString(action_environment)
                if len(action_environment) > 64:
                    action_environment = action_environment[:64]

            if th == "イラスト":
                illustration = td
                illustration = TrimString(illustration)
                if len(illustration) > 64:
                    illustration = illustration[:64]

            if th == "その他":
                others = td
                others = TrimString(others)
                if len(others) > 64:
                    others = others[:64]

            if th == "カップリング":
                coupling = td
                coupling = TrimString(coupling)
                if len(coupling) > 64:
                    coupling = coupling[:64]

        update_data = NowTime()

        # WorkDetails = WebData.find('div', class_="work_parts_area")
        # WorkDetails = WorkDetails.get_text()
        # while True:
        #     if "\n\n" in WorkDetails:
        #         WorkDetails = WorkDetails.replace("\n\n", "\n")
        #     else:
        #         break

        WorkDetails = ""
        tree = bs4.BeautifulSoup(html1.text, 'lxml')
        selector_table = tree.select('.work_parts_area')
        for item in selector_table:
            for i in item:
                if i == '\n':
                    continue
                data = i.text
                data = str(data)
                WorkDetails = WorkDetails + data
        if WorkDetails == "":
            selector_table = tree.select('.work_parts_multitype_item')
            for item in selector_table:
                for i in item:
                    if i == '\n':
                        continue
                    data = i.text
                    data = str(data)
                    WorkDetails = WorkDetails + data
        if "'" in WorkDetails:
            WorkDetails = WorkDetails.replace("'", "\\'")
        if '"' in WorkDetails:
            WorkDetails = WorkDetails.replace('"', '\\"')

        if WorkDetails == "":
            WorkDetails = None

        sql2 = f"INSERT INTO `works_full_information` " \
               f"(`work_id`, `work_type`, `tag`, `release_data`, `update_data`, `age_specification`, " \
               f"`work_format`, `file_format`, `event`, `file_capacity`, `voice_actor`, `scenario`, `author`, " \
               f"`series`, `page_number`, `language`, `music`, `action_environment`, `illustration`," \
               f"`others`, `coupling`, `img_path`, `work_details`)" \
               f" VALUES " \
               f"('{work_id}', '{work_type}', '{tag}', '{release_data}', '{update_data}', '{age_specification}', " \
               f"'{work_format}', '{file_format}', '{event}', '{capacity}', '{voice_actor}', '{scenario}', '{author}', " \
               f"'{series}', {page_number}, '{languages}', '{music}', '{action_environment}', '{illustration}'," \
               f"'{others}', '{coupling}', '{img_path}', '{WorkDetails}');"

        if "None" or "NULL" in sql2:
            sql2 = sql2.replace("None", "NULL")
            sql2 = sql2.replace("None", "NULL")
            sql2 = sql2.replace("'NULL'", "NULL")

        return IfRelease, sql2

    except Exception as e:
        print("错误信息:", str(e))
        print("错误类型:", type(e).__name__)
        _, _, tb = sys.exc_info()
        print("发生错误的位置:", tb.tb_frame.f_code.co_filename, "第", tb.tb_lineno, "行")
