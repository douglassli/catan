from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


def put_name(driver, name):
    name_input = driver.find_element_by_id("nameInput")
    name_input.send_keys(name)


def click_create(driver):
    create_button = driver.find_element_by_id("createRoomButton")
    create_button.send_keys(Keys.ENTER)


def click_ready(driver):
    mark_ready_button = driver.find_element_by_id("readyButton")
    mark_ready_button.send_keys(Keys.ENTER)


def get_room_id(driver):
    room_header = driver.find_element_by_id("roomHeader")
    return room_header.get_attribute("innerHTML").replace("Room ID: ", "")


def put_room_id(driver, room_id):
    room_input = driver.find_element_by_id("roomIdInput")
    room_input.send_keys(room_id)


def click_join(driver):
    join_button = driver.find_element_by_id("joinRoomButton")
    join_button.send_keys(Keys.ENTER)


def click_start(driver):
    start_button = driver.find_element_by_id("startButton")
    start_button.send_keys(Keys.ENTER)


def test1():
    d = wd.Safari()
    d.get("http://127.0.0.1:8080/room")
    d.execute_script("window.open('http://127.0.0.1:8080/room')")
    d.execute_script("window.open('http://127.0.0.1:8080/room')")
    d.execute_script("window.open('http://127.0.0.1:8080/room')")

    sizes = [(0, 23, 961, 527), (959, 23, 961, 527), (0, 550, 961, 527), (959, 550, 961, 527)]

    for i in range(4):
        d.switch_to.window(d.window_handles[i])
        time.sleep(0.25)
        d.set_window_rect(*sizes[i])

    d.switch_to.window(d.window_handles[0])
    time.sleep(0.25)
    put_name(d, "p1")
    click_create(d)
    rid = get_room_id(d)
    click_ready(d)

    for i in range(1, 4):
        d.switch_to.window(d.window_handles[i])
        time.sleep(0.25)
        put_name(d, "p{}".format(i + 1))
        put_room_id(d, rid)
        click_join(d)
        click_ready(d)

    click_start(d)

    x = input()


if __name__ == '__main__':
    test1()
