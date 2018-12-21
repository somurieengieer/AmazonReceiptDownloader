import os
from getpass import getpass
from time import sleep
from mylib import ChromeDriver
from mylib import Util

SAVE_DIR = "amazon_pdfs"
SAVE_FULL_DIR = os.getcwd() + "/" + SAVE_DIR  # ファイル保存先ディレクトリ

email = input('your Amazon e-Mail: ')
password = getpass("your Amazon password: ")


#ログイン処理を行う。
def login(driver):

    # AmazonID・パスワード入力ページ
    url_loginPage = 'https://www.amazon.co.jp//gp/navigation/redirector.html/ref=sign-in-redirect?ie=UTF8&amp;associationHandle=jpflex&amp;currentPageURL=https%3A%2F%2Fwww.amazon.co.jp%2F%3Fref_%3Dnav_custrec_signin&amp;pageType=Gateway&amp;switchAccount=&amp;yshURL=https%3A%2F%2Fwww.amazon.co.jp%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26ref_%3Dnav_custrec_signin'

    driver.get(url_loginPage)

    # (FYI) bellow line is same mean with -> driver.find_element_by_name("user_id").send_keys(email)
    driver.find_element_by_xpath('//*[@id="ap_email"]').send_keys(email)
    driver.find_element_by_xpath('//*[@id="ap_password"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="signInSubmit"]').click()
    sleep(3)

# 全領収書リンクへ遷移する
def clickReceiptLink(driver):
    divs = driver.find_elements_by_xpath('//*[@id="ordersContainer"]/div')
    size = len(divs)
    for i in range(size):
        divs = driver.find_elements_by_xpath('//*[@id="ordersContainer"]/div')
        try:
            # ダイレクトに「領収書／購入明細書」リンクがある場合
            divs[i].find_element_by_xpath('div[1]/div/div/div/div[2]/div[2]/ul/span[1]/a').click()
        except:
            try:
                # 「領収書等」クリック後に「領収書／購入明細書」リンクがある場合
                divs[i].find_element_by_xpath('div[1]/div/div/div/div[2]/div[2]/ul/span[1]/span/a').click()
                driver.find_element_by_xpath('//*[@class="a-popover-content"]/ul/li/span/a[contains(text(), "領収書／購入明細書")]').click()
#                driver.find_element_by_xpath('//*[@class="a-popover-content"]/ul/li[2]/span/a').click()

            except:
                print("exit[i=" + str(i) + "]")
                continue
        getReceipt(driver)

# 領収書を保存し、前の画面に戻る
def getReceipt(driver):
    try:
        orderDate = driver.find_element_by_xpath('/html/body/table[1]/tbody/tr/td/table[1]/tbody/tr/td[contains(., "注文日")]').text
    except:
        orderDate = driver.find_element_by_xpath('/html/body/div[1]/table[1]/tbody/tr[2]/td').text
    try:
        title = driver.find_element_by_xpath('/html/body/table[1]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td[1]/i').text
    except:
        try:
            # 「領収書等」クリック後に「領収書／購入明細書」リンクがある場合の領収書画面
            title = driver.find_element_by_xpath('/html/body/div[1]/table[2]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td[1]/b/a').text
        except:
            # アプリ用「領収書／購入明細書」リンクがある場合の領収書画面
            title = driver.find_element_by_xpath('/html/body/table[1]/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td[1]/i').text
    # 長いタイトルとスラッシュを削除
    title = title.replace('/', '')
    title = title[:20]

    # スクリーンショットの保存
    page_width = driver.execute_script('return document.body.scrollWidth')
    page_height = driver.execute_script('return document.body.scrollHeight') + 120
    driver.set_window_size(page_width, page_height)
    sleep(1)
    driver.save_screenshot(Util.pickDate(orderDate) + "_" + title + ".png")

    driver.back()

def goNextPage(driver):
    try:
        driver.find_element_by_xpath('//*[@id="ordersContainer"]/div/div/ul/li/a[contains(text(), "次へ")]').click()
        return True
    except:
        return False


def main():
    cDriver = ChromeDriver.ChromeDriver(saveDir=SAVE_FULL_DIR)
    driver = cDriver.getDriver()
    login(driver)

    # 注文履歴ページへ遷移
    driver.find_element_by_xpath('//*[@id="nav-orders"]/span[2]').click()

    while True:
        clickReceiptLink(driver)
        if not goNextPage(driver):
            break

main()