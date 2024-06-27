import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

class crawler(object):
    def __init__(self):
        self.salary = ['01','02','03','04','05','06','07','08','09','10','11','12']
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_job_info(self, number):
        job_data = []
        for salary in self.salary:
            url =f'https://we.51job.com/api/job/search-pc?' + \
                 f'&jobArea=020000' + \
                 f'&salary={salary}' + \
                 f'&pageNum={number}' + \
                 f'&pageCode=sou%7Csou%7Csoulb'
            self.driver.get(url)

            input("请手动完成滑块验证码，完成后按 Enter 继续：")

            pre_element = self.driver.find_element(By.TAG_NAME, 'pre')
            json_str = pre_element.get_attribute('textContent')

            try:
                json_dict = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"JSON decoding failed: {e}")
                json_dict = {}

            job_data += json_dict.get('resultbody', {}).get('job', {}).get('items', [])

            print(f"已完成第 {number} 页的数据爬取。")

        return job_data

if __name__ == '__main__':
    crawler = crawler()
    for i in range(1, 10):
        job_database = crawler.get_job_info(i)
        with open('shanghai.jsonl', 'a', encoding='utf-8') as f:
            for data in job_database:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
