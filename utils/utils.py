from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait_for(seconds):
    """Wait for the specified number of seconds."""
    try:
        seconds = int(seconds)
        sleep(seconds)
    except ValueError:
        print('Error: seconds must be a valid integer.')


# Exemplo de uso:
wait_for(5)  # Esperar por 5 segundos


def find_element(driver, by, value, timeout=10):
    """
    Encontrar um elemento na página usando espera explícita.
    """
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def find_elements(driver, by, value, timeout=10):
    """
    Encontrar elementos na página usando espera explícita.
    """
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((by, value))
    )


def is_element_present(driver, by, value, timeout=10):
    """
    Verificar se um elemento está presente na página.
    """
    try:
        find_element(driver, by, value, timeout)
        return True
    except Exception:
        return False


def is_element_displayed(driver, by, value, timeout=10):
    """
    Verificar se um elemento está visível na página.
    """
    try:
        element = find_element(driver, by, value, timeout)
        return element.is_displayed()
    except Exception:
        return False


def wait_for_element(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except Exception as e:
        raise TimeoutError(
            f'Tempo de espera excedido. Elemento não encontrado: {e}'
        )


def disable_element_by_class(driver, class_name, timeout=10):
    try:
        # Espera até que o elemento com a classe desejada apareça na página
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )

        # Usa JavaScript para modificar as propriedades CSS do elemento e desativá-lo
        driver.execute_script('arguments[0].remove();', element)
        return True
    except Exception as e:
        # Tratamento de exceção se o elemento não for encontrado ou se ocorrer outro erro
        print(f"Erro ao desativar elemento com classe '{class_name}': {e}")
        return False


def click_element(driver, by, value, timeout=10):
    """
    Clicar em um elemento na página.
    """
    element = find_element(driver, by, value, timeout)
    element.click()


def scroll_to_element_center(driver, element):
    """
    Rolar a página até um elemento centralizado.
    """
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", element
    )
