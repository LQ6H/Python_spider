#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H

from selenium import webdriver
import time

driver=webdriver.Chrome()
driver.maximize_window()

driver.get("https://www.douban.com/")

driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))

driver.find_element_by_xpath('//li[@class="account-tab-account"]').click()

driver.find_element_by_id('username').send_keys("18727549502")
driver.find_element_by_id('password').send_keys("LXQ1996@hacker")

driver.find_element_by_class_name('btn-account').click()

time.sleep(5)

driver.quit()