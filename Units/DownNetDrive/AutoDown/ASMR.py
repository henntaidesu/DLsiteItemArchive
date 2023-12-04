from Units.SQL.ALLSQL import *
from selenium import webdriver

def OpenASMRWEB():
    LimitData = '2023-10-01'
    sql1 = f"SELECT AS_work_updata_group.id ,works_full_information.work_id, works.work_name " \
           f"FROM works_full_information, AS_work_updata_group, works " \
           f"WHERE works_full_information.work_id = AS_work_updata_group.work_id " \
           f"AND works.work_id = works_full_information.work_id " \
           f"AND works_full_information.Release_data > '{LimitData}' " \
           f"AND works_full_information.work_type = 'SOU' " \
           f"AND AS_work_updata_group.group_name = 'Shine' " \
           f"AND works_full_information.tag lIKE '%耳かき%' " \
           f"AND AS_work_updata_group.url_state IN ('1', '2', '3', '4') " \
           f"AND works.work_state = '15'  " \
           f"GROUP BY works.work_name,  works_full_information.work_id, AS_work_updata_group.id " \
           f"Limit 1"
    Work = SelectAll(sql1)
    Work = Work[0]
    Id = Work[0]
    WorkId = Work[1]
    WorkName = Work[2]

    url = f'https://www.asmr.one/work/{WorkId}'
    print(url)

    # 启动Chrome浏览器
    driver = webdriver.Chrome()
    # 打开指定的URL
    driver.get(url)

    # 不要关闭浏览器，保持它打开
    input("按 Enter 键关闭浏览器...")

    # 关闭浏览器
    driver.quit()

    sql2 = f"update works set work_state = '-1' where work_id = '{WorkId}'"
    flag = UpdataAll(sql2)

