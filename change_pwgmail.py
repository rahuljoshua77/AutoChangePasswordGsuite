from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import random
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from faker import Faker
fake = Faker()
cwd = os.getcwd()

opts = Options()
opts.headless = False
opts.add_argument('log-level=3') 
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
opts.add_argument('--ignore-ssl-errors=yes')
opts.add_argument("--start-maximized")
opts.add_argument('--ignore-certificate-errors')
opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_experimental_option('excludeSwitches', ['enable-logging'])
path_browser = f"{cwd}\chromedriver.exe"

def change_pass():
    file_pw = "password.txt"
    pw_open = open(f"{cwd}/{file_pw}","r")
    get_pw = pw_open.read()
    new_password = get_pw.split()
    print(f"[*] [ {email} ] Trying to Change Password")
    element = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, "(//input[@type='password'])[1]")))
        
    element.send_keys(new_password)
    sleep(0.5)
    element = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, "(//input[@type='password'])[2]")))
        
    element.send_keys(new_password)

    try:
        wait(browser,5).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Ubah sandi')]"))).click()
    except:
        try:
            wait(browser,5).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Change password')]"))).click()
        except:
            element.send_keys(Keys.ENTER)
    try:
        wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/c-wiz/div/div[3]/div/div/header/div')))
        print(f"[*] [ {email} ] Success Change Password")
        with open('success_change.txt','a') as f:
            f.write('{0}|{1}\n'.format(email,new_password))
        browser.quit()
    except:
        print(f"[*] [ {email} ] Failed Change Password or Check Manual")
        with open('failed_change.txt','a') as f:
            f.write('{0}|{1}\n'.format(email,new_password))
        browser.quit()
def login_email(email, password):
    
    global element
    global browser
      
          
    sleep(5)
    element = wait(browser,15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#identifierId")))
    element.send_keys(email)
        
    sleep(0.5)
    element.send_keys(Keys.ENTER) 
    try:
        sleep(3)  
        element = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
        
        element.send_keys(password)
        sleep(0.5)
        element.send_keys(Keys.ENTER) 
    except:
        sleep(3)  
        element = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
        
        element.send_keys(password)
        sleep(0.5)
        element.send_keys(Keys.ENTER) 
    try: 
        wait(browser,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#accept"))).click()
    except:
        pass
    change_pass()
    

def open_browser(k):
    
    global browser
    global element
    global email
    global password
    k = k.split("|")
    email = k[0]
    password = k[1]
    random_angka = random.randint(100,999)
    random_angka_dua = random.randint(10,99)
    opts.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.{random_angka}.{random_angka_dua} Safari/537.36")
    browser = webdriver.Chrome(options=opts, desired_capabilities=dc, executable_path=path_browser)
    browser.get('https://accounts.google.com/signin/v2/challenge/pwd?continue=https%3A%2F%2Fmyaccount.google.com%2Fsigninoptions%2Fpassword%3Fcontinue%3Dhttps%3A%2F%2Fmyaccount.google.com%2Fsecurity&service=accountsettings&osid=1&rart=ANgoxcff6zbrLbWstaY-9fVSFsTKO5fAgdVpbDKiBY7nWnC3ifanwpN02VubsmACogKzFiW81J17wHg8QJuEwHwT9kMt_zflPw&TL=AM3QAYbdQJE_fF5FQRYR7ZB-l_JagNlyY4uTef6LkothrQb5PIEfDqdmreSUqNZd&flowName=GlifWebSignIn&cid=1&flowEntry=ServiceLogin')
    
    print(f"[*] [ {email} ] Trying to Login")
    login_email(email, password)

if __name__ == '__main__':
    global list_accountsplit
    print('[*] Automation Change Password GMail')
    print('[*] Author: RJD')
    jumlah = int(input("[*] Multi Processing: "))
    password_fill = input("[*] New Password: ")
    with open('password.txt','w') as f:
        f.write('{0}'.format(password_fill))
    file_list_akun = "list_email.txt"
    myfile_akun = open(f"{cwd}/{file_list_akun}","r")
    akun = myfile_akun.read()
    list_accountsplit = akun.split()
    k = list_accountsplit
    with Pool(jumlah) as p:  
        p.map(open_browser, k)
    print('[*] Automation is Done')
