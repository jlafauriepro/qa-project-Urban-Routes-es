import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    call_taxi_button = (By.XPATH, './/button[@class="button round"]')
    comfort_tariff = (By.XPATH, './/div[@class="tcard-title" and text()="Comfort"]')
    phone_number_button = (By.CLASS_NAME, 'np-button')
    phone_number_field = (By.ID, 'phone')
    next_button = (By.XPATH, './/button[@type="submit" and @class="button full" and text()="Siguiente"]')
    sms_code_field = (By.ID, 'code')
    confirm_button = (By.XPATH, './/button[@type="submit" and text()="Confirmar"]')
    payment_method_button = (By.CLASS_NAME, 'pp-button')
    add_card_button = (By.XPATH, './/div[@class="pp-title" and text()="Agregar tarjeta"]')
    card_number_field = (By.ID, 'number')
    card_code_field = (By.CSS_SELECTOR, 'input.card-input#code')
    add_button = (By.XPATH, './/button[@type="submit" and text()="Agregar"]')
    close_payment_modal = (By.XPATH, './/div[contains(@class,"payment-picker")]//button[contains(@class,"section-close")]')
    message_field = (By.ID, 'comment')
    blanket_switch = (By.CSS_SELECTOR, 'span.slider.round')
    ice_cream_plus = (By.CLASS_NAME, 'counter-plus')
    order_button = (By.CLASS_NAME, 'smart-button')
    order_modal = (By.CLASS_NAME, 'order-header-title')

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            expected_conditions.visibility_of_element_located(locator)
        )

    def wait_for_element_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            expected_conditions.element_to_be_clickable(locator)
        )

    def set_from(self, from_address):
        self.wait_for_element_visible(self.from_field)
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def click_call_taxi_button(self):
        self.wait_for_element_clickable(self.call_taxi_button)
        self.driver.find_element(*self.call_taxi_button).click()

    def select_comfort_tariff(self):
        self.wait_for_element_clickable(self.comfort_tariff)
        self.driver.find_element(*self.comfort_tariff).click()

    def click_phone_number_button(self):
        self.wait_for_element_clickable(self.phone_number_button)
        self.driver.execute_script("arguments[0].click();",
                                   self.driver.find_element(*self.phone_number_button))

    def set_phone_number(self, phone_number):
        self.wait_for_element_visible(self.phone_number_field)
        self.driver.find_element(*self.phone_number_field).send_keys(phone_number)

    def click_next_button(self):
        self.wait_for_element_clickable(self.next_button)
        self.driver.find_element(*self.next_button).click()

    def set_sms_code(self, code):
        self.wait_for_element_visible(self.sms_code_field)
        self.driver.find_element(*self.sms_code_field).send_keys(code)

    def click_confirm_button(self):
        self.wait_for_element_clickable(self.confirm_button)
        self.driver.find_element(*self.confirm_button).click()

    def click_payment_method_button(self):
        self.wait_for_element_clickable(self.payment_method_button)
        self.driver.execute_script("arguments[0].click();",
                                   self.driver.find_element(*self.payment_method_button))

    def click_add_card_button(self):
        self.wait_for_element_clickable(self.add_card_button)
        self.driver.find_element(*self.add_card_button).click()

    def set_card_number(self, card_number):
        self.wait_for_element_visible(self.card_number_field)
        self.driver.find_element(*self.card_number_field).send_keys(card_number)

    def set_card_code(self, card_code):
        self.wait_for_element_visible(self.card_code_field)
        field = self.driver.find_element(*self.card_code_field)
        field.send_keys(card_code)
        field.send_keys(Keys.TAB)

    def click_add_button(self):
        self.wait_for_element_clickable(self.add_button)
        self.driver.find_element(*self.add_button).click()

    def close_payment_modal_button(self):
        self.wait_for_element_visible(self.close_payment_modal)
        self.driver.find_element(*self.close_payment_modal).click()

    def set_message_for_driver(self, message):
        self.wait_for_element_visible(self.message_field)
        self.driver.find_element(*self.message_field).send_keys(message)

    def click_blanket_switch(self):
        self.wait_for_element_clickable(self.blanket_switch)
        self.driver.execute_script("arguments[0].click();",
                                   self.driver.find_element(*self.blanket_switch))

    def click_ice_cream_plus(self, times=2):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.invisibility_of_element_located((By.CLASS_NAME, 'overlay'))
        )
        self.wait_for_element_clickable(self.ice_cream_plus)
        for _ in range(times):
            self.driver.find_element(*self.ice_cream_plus).click()

    def click_order_button(self):
        self.wait_for_element_clickable(self.order_button)
        self.driver.find_element(*self.order_button).click()

    def check_order_modal_appears(self):
        return self.wait_for_element_visible(self.order_modal)


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        options = webdriver.ChromeOptions()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    def test_select_comfort_tariff(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_call_taxi_button()
        routes_page.select_comfort_tariff()

    def test_set_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_phone_number_button()
        routes_page.set_phone_number(data.phone_number)
        routes_page.click_next_button()
        phone_code = retrieve_phone_code(self.driver)
        routes_page.set_sms_code(phone_code)
        routes_page.click_confirm_button()

    def test_add_credit_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_payment_method_button()
        routes_page.click_add_card_button()
        routes_page.set_card_number(data.card_number)
        routes_page.set_card_code(data.card_code)
        routes_page.click_add_button()
        routes_page.close_payment_modal_button()

    def test_set_message_for_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_message_for_driver(data.message_for_driver)

    def test_order_blanket_and_tissues(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_blanket_switch()

    def test_order_ice_cream(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_ice_cream_plus(2)

    def test_order_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_order_button()
        modal = routes_page.check_order_modal_appears()
        assert modal is not None

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()