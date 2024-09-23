from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time

# GeckoDriver的路径（请根据实际情况替换路径）
GECKO_DRIVER_PATH = 'D:/feelLLM/src/geckodriver.exe'  # 替换为您的GeckoDriver路径

def extract_article_text_with_firefox(article_url):
    """使用Selenium与Firefox提取新闻文本"""
    try:
        # 配置Selenium WebDriver
        service = Service(GECKO_DRIVER_PATH)
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')  # 无头模式，后台运行浏览器
        driver = webdriver.Firefox(service=service, options=options)
        
        # 访问目标URL
        driver.get(article_url)
        time.sleep(5)  # 等待页面加载，您可以调整等待时间

        # 使用Selenium查找内容
        content_div = driver.find_element(By.CLASS_NAME, 'description-body')
        paragraphs = content_div.find_elements(By.TAG_NAME, 'p')
        article_text = '\n'.join([para.text for para in paragraphs])
        
        # 关闭浏览器
        driver.quit()
        
        return article_text.strip()
    except Exception as e:
        print(f"无法提取URL {article_url} 的内容: {e}")
        return None

# 示例用法
article_url = 'https://cryptopanic.com/news/19924631/This-Ethereum-Token-Is-Set-To-Replicate-Dogecoin-And-Shiba-Inu-Millionaire-Run-From-2021'
article_text = extract_article_text_with_firefox(article_url)
if article_text:
    print("提取的新闻内容:\n", article_text)
else:
    print("未能提取新闻内容。")
