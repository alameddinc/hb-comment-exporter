import os
import time

import dotenv
import pandas as pd
from selenium.webdriver import Safari


class HepsiburadaCommentExtractor:
    def __init__(self):
        self.username = os.environ.get("HEPSIBURADA_USERNAME")
        self.password = os.environ.get("HEPSIBURADA_PASSWORD")
        self.driver = Safari()
        self.driver.get("https://www.hepsiburada.com/stanley-adventure-switchback-termos-bardak-0-47-lt-p-HBV00000LE61I-yorumlari?sayfa=2")
        time.sleep(1)
        comments = self.get_comments()
        ## write to csv
        comments.to_csv("comments.csv")





    def get_comments(self):
        df = pd.DataFrame(columns=["comment", "rating"])
        ## /html/body/div[2]/main/div[2]/div/div/div/div/div/div/div[1]/div[2]/div/div[6]/div[3]/div[2]/div/ul/li[9]/span
        page_count = int(self.driver.find_element_by_xpath("/html/body/div[2]/main/div[2]/div/div/div/div/div/div/div[1]/div[2]/div/div[6]/div[3]/div[2]/div/ul/li[9]/span").text)
        #https://www.hepsiburada.com/nespresso-f121-one-lattissima-kahve-makinesi-siyah-p-HBCV00000MOC74-yorumlari?magaza=UzayEticaret/&sayfa=2

        for i in range(1, page_count+1):
            self.driver.get(f"https://www.hepsiburada.com/stanley-adventure-switchback-termos-bardak-0-47-lt-p-HBV00000LE61I-yorumlari?sayfa={i}")
            time.sleep(1)
            ## //*[@id="hermes-voltran-comments"]/div[6]/div[3]/div[1]/div
            comments = self.driver.find_elements_by_xpath("//*[@id='hermes-voltran-comments']/div[6]/div[3]/div[1]/div")
            print(i)
            for comment in comments:
                ## Text = //*[@id="hermes-voltran-comments"]/div[5]/div[3]/div/div[1]/div[2]/div[2]/span
                ### blank webelement for textbody
                if not comment.find_elements_by_xpath("./div[2]/div[2]/span"):
                    continue
                text_body = comment.find_element_by_xpath("./div[2]/div[2]/span").text
                ## //*[@id="hermes-voltran-comments"]/div[5]/div[3]/div/div[1]/div[2]/div[1]/div[2]/div/span/div
                star_div = comment.find_element_by_xpath("./div[2]/div[1]/div[2]/div/span/div")
                ##  class name star and outlinedStar for star count
                star_count = len(star_div.find_elements_by_class_name("star"))
                df = df.append({"comment": text_body, "rating": star_count}, ignore_index=True)
        return df

    def close(self):
        self.driver.close()

    def run(self, keyword):
        self.login()
        self.search(keyword)
        comments = []
        for i in range(1, 6):
            comments += self.get_comments()
            self.next_page()
        self.close()
        return comments

if __name__ == "__main__":
    dotenv.load_dotenv()
    extractor = HepsiburadaCommentExtractor()
