# 代码来源：https://github.com/huabench/github-workflow-zhihu/blob/main/src/generate_zhihu_badge.py
# 原作者：huabench

import requests
from bs4 import BeautifulSoup
import re
import os

# 假设你使用 shields.io 生成 badge
SHIELDS_IO_URL = "https://img.shields.io/badge/dynamic/json"

def get_data_by_tag(soup, attr):
    meta_tag = soup.find('meta', attrs={'itemprop': attr})
    count = int(meta_tag['content']) if meta_tag else None
    return count

def get_zhihu_data(username):
    url = f"https://www.zhihu.com/people/{username}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }
    # 发送 GET 请求
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        follower_count = get_data_by_tag(soup, 'zhihu:followerCount')
        voteup_count = get_data_by_tag(soup, 'zhihu:voteupCount')
        thanked_count = get_data_by_tag(soup, 'zhihu:thankedCount')

        return follower_count, voteup_count, thanked_count
    else:
        raise Exception("Error fetching Zhihu followers data")
    
def generate_badge(data, label):
    return f"https://img.shields.io/badge/{data}-blue?logo=zhihu&logoColor=blue&label={label}&labelColor=white&color=blue"
  
def update_readme(badge_url, label):
    with open('README.md', 'r+') as readme:
        content = readme.read()
        # 这里的正则表达式需要根据你的 README.md 中 badge 的 markdown 格式调整
        updated_content = re.sub(f'https://img\\.shields\\.io/badge/\\S+?logo=zhihu\\S+label={label}[^"]+', badge_url, content)
        readme.seek(0)
        readme.write(updated_content)
        readme.truncate() # 用于删除文件的剩余部分

if __name__ == '__main__':
    username = os.environ.get('ZHIHU_USERNAME')
    data = get_zhihu_data(username)
    labels = ["Follower", "Voteup", "Thanked"]
    for count, label in zip(data, labels):
        badge_url = generate_badge(count, label)
        update_readme(badge_url, label)
