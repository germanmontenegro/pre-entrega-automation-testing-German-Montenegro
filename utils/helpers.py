"""
Funciones auxiliares para los tests de saucedemo.com.

Contiene:
- Constantes (URL, credenciales y localizadores).
- Creación del driver de Chrome.
- Funciones reutilizables: login, espera de elementos, logging.
"""
import logging
import os
import sys

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
BASE_URL = "https://www.saucedemo.com/"
INVENTORY_URL_FRAGMENT = "/inventory.html"
CART_URL_FRAGMENT = "/cart.html"
USUARIO_VALIDO = "standard_user"
PASSWORD_VALIDO = "secret_sauce"
TIMEOUT = 10  # segundos para las esperas explícitas

# Localizadores (By, valor)
USERNAME_INPUT = (By.ID, "user-name")
PASSWORD_INPUT = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")
PAGE_TITLE = (By.CLASS_NAME, "title")  # texto "Products"
APP_LOGO = (By.CLASS_NAME, "app_logo")  # texto "Swag Labs"
INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
MENU_BUTTON = (By.ID, "react-burger-menu-btn")
SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
CART_ITEMS = (By.CLASS_NAME, "cart_item")
ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[id^='add-to-cart']")

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
os.makedirs("reports", exist_ok=True)
logger = logging.getLogger("saucedemo")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def crear_driver():
    """Crea una instancia de Chrome.

    Si la variable de entorno HEADLESS=1 está definida, corre sin ventana
    (útil en servidores / CI). Selenium Manager descarga el chromedriver
    automáticamente (Selenium >= 4.6).
    """
    opciones = Options()
    if os.getenv("HEADLESS") == "1":
        opciones.add_argument("--headless=new")
        opciones.add_argument("--window-size=1920,1080")
    else:
        opciones.add_argument("--start-maximized")
    # Estos flags solo hacen falta en Linux (servidores / contenedores);
    # en Windows pueden hacer que Chrome se cierre al iniciar.
    if sys.platform.startswith("linux"):
        opciones.add_argument("--no-sandbox")
        opciones.add_argument("--disable-dev-shm-usage")
    # Evita el popup de "cambiar contraseña" de Chrome que tapa la página
    opciones.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        },
    )
    try:
        return webdriver.Chrome(options=opciones)
    except WebDriverException as error:
        # Plan B: si Chrome no arranca, probamos con Microsoft Edge
        # (viene instalado en Windows 10/11).
        logger.warning("Chrome no pudo iniciar (%s). Probando con Edge...", error.msg)
        opciones_edge = EdgeOptions()
        if os.getenv("HEADLESS") == "1":
            opciones_edge.add_argument("--headless=new")
        else:
            opciones_edge.add_argument("--start-maximized")
        return webdriver.Edge(options=opciones_edge)


# ---------------------------------------------------------------------------
# Funciones reutilizables
# ---------------------------------------------------------------------------
def esperar_visible(driver, localizador, timeout=TIMEOUT):
    """Espera explícitamente a que un elemento sea visible y lo devuelve."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(localizador)
    )


def esperar_clickeable(driver, localizador, timeout=TIMEOUT):
    """Espera explícitamente a que un elemento sea clickeable y lo devuelve."""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(localizador)
    )


def hacer_login(driver, usuario=USUARIO_VALIDO, password=PASSWORD_VALIDO):
    """Abre la página de login e inicia sesión con las credenciales dadas.

    Espera explícitamente a que cargue el formulario y, tras el click,
    a que la URL contenga /inventory.html.
    """
    logger.info("Navegando a %s", BASE_URL)
    driver.get(BASE_URL)
    esperar_visible(driver, USERNAME_INPUT).send_keys(usuario)
    driver.find_element(*PASSWORD_INPUT).send_keys(password)
    esperar_clickeable(driver, LOGIN_BUTTON).click()
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains(INVENTORY_URL_FRAGMENT))
    logger.info("Login exitoso con el usuario '%s'", usuario)
