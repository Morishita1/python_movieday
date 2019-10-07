from bs4 import BeautifulSoup
from selenium import webdriver
import persistence.MongoDAO as DAO
import requests

class DaumCrawler():
    def __init__(self):
        self.mDao = DAO.MongoDAO() # 객체생성

    def crawler(self, code):

        # 페이지 존재유무 체크
        doc = requests.get('https://movie.daum.net/moviedb/main?movieId={}').format(code)
        if doc.status_code != 200: # 200(success)
            print('>> Not Found Page:/')
            return

        path = 'E:\Bigdata\webdriver\chromedriver.exe'
        driver = webdriver.Chrome(path)

        # 웹 크롤링
        page = 1
        count = 0
        while True:
            url = 'https://movie.daum.net/moviedb/grade?movieId={}&type=netizen&page={}'.format(code, page)
            driver.get(url)  # http:// 까지 적어야함
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            reply_list = soup.select('div.main_detail ul.list_review.list_netizen li')

            if reply_list == []:
                break

            for reply in reply_list:
                writer = reply.select('div.review_info a em')[0].text
                cont = reply.select('div.review_info p.desc_review')[0].text.strip()
                star_score = reply.select('div.review_info div.raking_grade em')[0].text
                reg_date = reply.select('div.review_info div.append_review span.info_append')[0].text.strip()[:10]

                data = {'star_score': star_score, 'writer': writer, 'cont': cont, 'reg_date': reg_date}

                # MongoDB에 댓글 저장
                self.mDao.mongo_write(data)

                print(
                    '▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒')
                print('작성자 : ', writer)
                print('내용 : ', cont)
                print('평점 : ', star_score)
                print('작성일자 : ', reg_date)
                count += 1
            print('>>>>>>>>>>>>>>', page, '페이지 수집함')
            page += 1
        driver.close()
        print('▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒')
        print('수집한 게시글 수는 {}건입니다.'.format(count))