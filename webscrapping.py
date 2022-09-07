def chrome_searcher_nomecao_decide(day_input):
    
    from selenium import webdriver
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.common.exceptions import ElementNotVisibleException
    import os
    import time

    
    for filename in os.listdir(os.path.abspath(os.getcwd())):
        if filename == 'chromedriver.exe':
            driver_exe = filename
    
    done = "Done"
    chromeOptions = webdriver.ChromeOptions()

    #where to download:
    prefs = {"download.default_directory" :r"{}\games_info".format(os.path.abspath(os.getcwd()))}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromedriver = "path/to/chromedriver.exe"
    #path of the webdriver executer:
    driver = webdriver.Chrome(executable_path=r'{fname}\\{driver_exe}'.format(fname=os.path.abspath(os.getcwd()),driver_exe=driver_exe), chrome_options=chromeOptions)


    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.get('https://afsetubal.fpf.pt/Associa%C3%A7%C3%A3o/Documenta%C3%A7%C3%A3o/Nomea%C3%A7%C3%B5es-de-%C3%81rbitros')
    wait = WebDriverWait(driver,10)

    #driver = webdriver.Chrome(executable_path=r'{fname}\\{driver_exe}'.format(fname=os.path.abspath(os.getcwd()),driver_exe=driver_exe))

    m=0
    n=0

    try:

        button = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/div[3]/div[1]/div/div[2]")
        button.click()

        time.sleep(2)

        #Displays invisible elements:
        container = driver.find_element(By.XPATH,"/html/body/form/div[3]/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/div[3]/div[1]/div/div[2]/select")
        driver.execute_script("arguments[0].style.display = 'block';", container)

        #Select element:
        select = Select(driver.find_element(By.XPATH,"/html/body/form/div[3]/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/div[3]/div[1]/div/div[2]/select"))
        select.select_by_visible_text('Todas as épocas')

        #Click ok to select "Todas as Épocas"
        button_2= driver.find_element(By.ID, "btnSearch")
        button_2.click()
        
        time.sleep(1)

        #Day of the Nomeação:
        day = str(day_input)
        if len(day) == 1:
            day = '0'+ day

        #driver find documents
        att = driver.find_element(By.XPATH,"//div[@class='list-content list-documents clearFloats']")

        tab_att=att.get_attribute('innerHTML')
        tab_att=tab_att.split()
        for i in tab_att:
            if 'date' in i:
                i = i.split('>')
                i = i[1]
                n+=1
                day = str(day)
                if i == day:
                    xpath = "/html/body/form/div[3]/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/div[3]/div[2]/div[{index}]/div/a".format(index=n)
                    nomeacao_date = driver.find_element(By.XPATH,xpath)
                    nomeacao_date.click()
                    time.sleep(1)
                    return done
                
    except Exception as e:
        print(e)

    return None


def chrome_searcher_last_nomeacao():

    from selenium import webdriver
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.common.exceptions import ElementNotVisibleException
    import os
    import time

    for filename in os.listdir(os.path.abspath(os.getcwd())):
        if filename == 'chromedriver.exe':
            driver_exe = filename

    done = "Done"
    chromeOptions = webdriver.ChromeOptions()

    #where to download:
    prefs = {"download.default_directory" :r"{}\games_info".format(os.path.abspath(os.getcwd()))}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromedriver = "path/to/chromedriver.exe"
    #path of the webdriver executer:
    driver = webdriver.Chrome(executable_path=r'{fname}\\{driver_exe}'.format(fname=os.path.abspath(os.getcwd()),driver_exe=driver_exe), chrome_options=chromeOptions)


    driver.maximize_window()
    driver.implicitly_wait(1)
    driver.get('https://afsetubal.fpf.pt/Associa%C3%A7%C3%A3o/Documenta%C3%A7%C3%A3o/Nomea%C3%A7%C3%B5es-de-%C3%81rbitros')
    wait = WebDriverWait(driver,5)
    
    try:

        button = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/div[3]/div[1]/div/div[2]")
        button.click()

        time.sleep(2)

        #Displays invisible elements:
        container = driver.find_element(By.XPATH,"/html/body/form/div[3]/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/div[3]/div[1]/div/div[2]/select")
        driver.execute_script("arguments[0].style.display = 'block';", container)

        #Select element:
        select = Select(driver.find_element(By.XPATH,"/html/body/form/div[3]/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/div[3]/div[1]/div/div[2]/select"))
        select.select_by_visible_text('Todas as épocas')

        #Click ok to select "Todas as Épocas"
        button_2= driver.find_element(By.ID, "btnSearch")
        button_2.click()

        time.sleep(1)

        #Day of the Nomeação:
        nomeacao_date = driver.find_element(By.XPATH,'/html/body/form/div[3]/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/div[3]/div[2]/div[1]/div/a')
        
        nomeacao_date.click()
        time.sleep(1)
        
        return done
        
    except Exception as e:
        print(e)    
