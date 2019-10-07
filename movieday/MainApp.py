import collector.DaumCrawler as collector

code = '127878' # 다음 영화코드

# 다음영화 수집 Start!!!
try:
    scrapy = collector.DaumCrawler() # 객체 생성
    scrapy.crawler(code)
except Exception as e:
    print('>> Exception(')
    print('>>',e)
finally:
    pass