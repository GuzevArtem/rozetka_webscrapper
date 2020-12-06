from selenium import webdriver 
import settings

class Driver:
    driver = webdriver.Chrome()
    closed = True

    def get() :
        if Driver.driver is None:
            return Driver.createDriver(settings.DEFAULT_SELENIUM_DRIVER)
        return Driver.driver

    def createDriver(driver_name = "chrome"):
        driverMap = { #lambda to prevent pre creating of objects
            "firefox" : lambda : webdriver.Firefox(),
            "chrome" : lambda : webdriver.Chrome(),
            "edge" : lambda : webdriver.Edge(),
            "safari" : lambda : webdriver.Safari()
            }
        try:
            Driver.driver = driverMap[lower(driver_name)]()
        except KeyError as e:
            print ( "Webdriver with name:", driver_name, "Not found. Chrome will be used as default. (Also Edge, Safari, Firefox could be used. More info at: https://selenium-python.readthedocs.io/installation.html#detailed-instructions-for-windows-users)")
            Driver.driver = webdriver.Chrome()
        Driver.closed = False
        return Driver.driver

    def close() :
        if Driver.driver is not None:
            Driver.driver.close()
        Driver.closed = True

    def quit() :
        if Driver.driver is not None:
            if Driver.closed is False:
                Driver.close()
            Driver.driver.quit()
            Driver.driver = None
        
        
