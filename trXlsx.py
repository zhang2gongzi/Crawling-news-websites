import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 目标网站的主页链接
base_url = "https://www.rmzxb.com.cn/rs/ffdt/index_12.shtml"
# 获取主页面内容
response = requests.get(base_url)
response.encoding = 'utf-8'  # 设置编码
soup = BeautifulSoup(response.text, 'html.parser')

# 提取 <div class="pa_0_15"> 中的 <a> 标签链接
articles = []
for div in soup.find_all('div', class_='pa_0_15'):
    for a_tag in div.find_all('a'):
        if 'href' in a_tag.attrs:
            link = a_tag['href']
            # 检查链接是否为完整链接
            if not link.startswith("http"):
                link = "https://www.rmzxb.com.cn" + link
            title = a_tag.text.strip()  # 获取文章标题
            articles.append({"title": title, "link": link})

# 爬取每个文章链接的内容
def fetch_article_content(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'  # 设置编码
        article_soup = BeautifulSoup(response.text, 'html.parser')
        # 查找 <div class="text_box"> 中的内容
        text_box_div = article_soup.find('div', class_='text_box')
        if text_box_div:
            article_content = text_box_div.get_text(separator=' ', strip=True)
            return article_content
        else:
            return "未找到文章内容"
    except Exception as e:
        print(f"无法抓取 {url}: {e}")
        return ""

# 抓取每篇文章的内容并存储
for article in articles:
    print(f"正在抓取: {article['title']} - {article['link']}")
    article['content'] = fetch_article_content(article['link'])
    time.sleep(1)  # 延迟，避免过快的请求

# 保存结果到 Excel 文件
df = pd.DataFrame(articles)
df.to_excel('rmzxb_articles.xlsx', index=False)
print("所有数据已保存到 rmzxb_articles.xlsx 文件中")
