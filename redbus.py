import time
from selenium import webdriver
import input_handler
from selenium.webdriver.common.by import By
import Packages.postgres_dbconnect as db_connectivity
from Packages.settings import OPTIONS, CONFIG, DOWNLOAD_PATH, LOGGER, CustomException, XpathMismatch
import datetime



def login():
    today = datetime.date.today()
    date_format = today.strftime('%d-%b-%Y')

    driver = webdriver.Chrome(options=OPTIONS)
    url = r'https://www.redbus.in'
    driver.get(url)
    driver.implicitly_wait(10)
    try:
        input_handler.processing_check_wait(driver, CONFIG.get('REDBUS_XPATHS', 'source'), 20)
        input_handler.choose_drop_down_enter(driver, CONFIG.get('REDBUS_XPATHS', 'bus_item_details'), CONFIG.get('REDBUS_XPATHS', 'source_element'),"Tirupati",1)
    except XpathMismatch:
        raise XpathMismatch("Failed to entire source")


        # raise "Failed to entire source"
        # print("Failed to entire source")
    input_handler.processing_check_wait(driver, CONFIG.get('REDBUS_XPATHS', 'destination'), 20)
    input_handler.choose_drop_down_enter(driver, CONFIG.get('REDBUS_XPATHS', 'destination'), CONFIG.get('REDBUS_XPATHS', 'destination_element'),"Hyderabad",3)

    input_handler.processing_check_wait(driver, CONFIG.get('REDBUS_XPATHS', 'date'), 20)
    try:
        # remove the read only option in From Date
        driver.execute_script(
            "document.getElementById('onward_cal')"
            ".removeAttribute('readonly',0);")
        input_handler.mouse_click_send_keys(driver, CONFIG.get('REDBUS_XPATHS', 'date'), date_format, 5)
    except Exception as err_or:
        err = "could not make from date readonly"



    # input_handler.mouse_click(driver, CONFIG.get('REDBUS_XPATHS', 'date'), 3)
    #
    # input_handler.processing_check_wait(driver, CONFIG.get('REDBUS_XPATHS', 'current_date'), 20)
    # input_handler.mouse_click(driver, CONFIG.get('REDBUS_XPATHS', 'current_date'), 3)
    time.sleep(3)

    input_handler.processing_check_wait(driver, CONFIG.get('REDBUS_XPATHS', 'search'), 20)
    input_handler.mouse_click(driver, CONFIG.get('REDBUS_XPATHS', 'search'), 3)
    time.sleep(7)

    while True:
        input_handler.scroll(driver, 2000)
        if input_handler.processing_check_wait(driver, CONFIG.get('REDBUS_XPATHS', 'scroll_down'), 2):
            break
    # //span[text()=' 2023 ibibogroup All rights reserved']
    # ((//div[@class ="clearfix bus-item-details"])[1]//div/div[4])/div[1]

    rows = driver.find_elements(By.XPATH, CONFIG.get('REDBUS_XPATHS', 'bus_item_details'))
    # bus_dict = {}
    for row in range(1, len(rows)+1):
        bus_dict = {}
        bus_dict['bus_name'] = driver.find_element(By.XPATH, (CONFIG.get('REDBUS_XPATHS', 'bus_name_1') + '['+str(row)+']' + CONFIG.get('REDBUS_XPATHS', 'bus_name_2'))).text
        bus_dict['arrival'] = driver.find_element(By.XPATH, (CONFIG.get('REDBUS_XPATHS', 'arrival_1')+'['+str(row)+']'+ CONFIG.get('REDBUS_XPATHS', 'arrival_2'))).text
        bus_dict['departure'] = driver.find_element(By.XPATH, (CONFIG.get('REDBUS_XPATHS', 'departure_1')+'['+str(row)+']'+CONFIG.get('REDBUS_XPATHS', 'departure_2'))).text
        bus_dict['price'] = driver.find_element(By.XPATH, (CONFIG.get('REDBUS_XPATHS', 'price_1') + '['+str(row)+']' + CONFIG.get('REDBUS_XPATHS', 'price_2'))).text
        bus_dict['status'] = 'none'
        # bus_data_list.append(bus_dict)

        try:
            db_connectivity.insert_dict_to_table('red_bus', bus_dict)
        except Exception as e:
            print(e)


login()



    # col_name = ['bus_name', 'arrival', 'departure', 'price', 'status']
    # value_list = [tuple(i.values() for i in bus_data_list)]
    # print(value_list)
    # headers = list(i.keys() for i in bus_data_list)
    # print(headers)
    # busname =[]
    # arr =[]
    # dep =[]
    # pri= []
    # stat=['none' for i in range(len(rows))]
    # for row in range(1, len(rows) + 1):
    #     busname.append(driver.find_element(By.XPATH, '((//div[@class ="clearfix bus-item-details"])['+str(row)+']/div/div/div)[1]').text)
    #     arr.append(driver.find_element(By.XPATH, '((//div[@class ="clearfix bus-item-details"])['+str(row)+']//div/div[4])/div[1]').text)
    #     dep.append(driver.find_element(By.XPATH, '((//div[@class ="clearfix bus-item-details"])['+str(row)+']//div/div[2])/div[1]').text)
    #     pri.append(driver.find_element(By.XPATH, '(//div[@class ="clearfix bus-item-details"])['+str(row)+']//div[@class="fare d-block"]/span').text)
    #
    # a = [busname, arr, dep, pri, stat]
    # col_name = ['bus_name', 'arrival','departure', 'price', 'status']
    # dict_bus= dict(zip(col_name,a))

# '+str(row)+'















