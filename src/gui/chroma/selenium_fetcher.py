
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class SeleniumFetcher:
    @staticmethod
    def extract_colors(section_title, driver):
        try:
            section = driver.find_element(By.XPATH, f"//h3[text()='{section_title}']")
            description = section.find_element(By.XPATH, "following-sibling::p").text.strip()
            color_elements = section.find_element(By.XPATH, "following-sibling::div").find_elements(By.CLASS_NAME, "color")
            colors = [color.get_attribute("data-copycolor") for color in color_elements]
            return {"description": description, "colors": colors}
        except Exception as e:
            print(f"Error extracting {section_title}: {e}")
            return {"description": "", "colors": []}

    def fetch_color_data(self, hex_code: str) -> dict:
        options = Options()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)

        formatted_hex_code = hex_code.lstrip('#')
        url = f'https://colorkit.co/color/{formatted_hex_code}/'
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        main_display = wait.until(EC.visibility_of_element_located((By.ID, "main-display")))

        color_name = main_display.find_element(By.XPATH, ".//div[@style='font-size:1.6em;font-weight:bold;']").text
        color_code = main_display.find_element(By.XPATH, ".//div[@style='font-size:1.3em']/span").get_attribute("data-copycolor")
        color_name_snake = color_name.lower().replace(' ', '_')

        sections = [
            'Brighten',
            'Darken',
            'Desaturate',
            'Hue',
            'Analogous',
            'Monochromatic',
            'Complementary',
            'Split Complement',
            'Triad',
            'Tetrad',
        ]

        color_data = {section: self.extract_colors(section, driver) for section in sections}
        color_data["name"] = color_name
        color_data["code"] = color_code

        driver.quit()

        return color_name_snake, color_data
