"""
Pre-entrega: automatización de saucedemo.com con Selenium + Pytest.

Casos de prueba:
1. Login exitoso.
2. Navegación y verificación del catálogo.
3. Interacción con productos (carrito).

Cada test usa su propio navegador (fixture `driver`), por lo que son
independientes entre sí.
"""
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.helpers import (
    ADD_TO_CART_BUTTON,
    APP_LOGO,
    CART_BADGE,
    CART_ITEMS,
    CART_LINK,
    CART_URL_FRAGMENT,
    INVENTORY_ITEMS,
    INVENTORY_URL_FRAGMENT,
    ITEM_NAME,
    ITEM_PRICE,
    MENU_BUTTON,
    PAGE_TITLE,
    SORT_DROPDOWN,
    TIMEOUT,
    esperar_clickeable,
    esperar_visible,
    hacer_login,
)

logger = logging.getLogger("saucedemo")


# ---------------------------------------------------------------------------
# 1. Login
# ---------------------------------------------------------------------------
def test_login_exitoso(driver):
    """Login con credenciales válidas y redirección a /inventory.html."""
    hacer_login(driver)

    # La URL debe contener /inventory.html
    assert INVENTORY_URL_FRAGMENT in driver.current_url, (
        f"No se redirigió a la página de inventario. URL actual: {driver.current_url}"
    )

    # El encabezado debe decir "Products" y el logo "Swag Labs"
    titulo = esperar_visible(driver, PAGE_TITLE).text
    logo = esperar_visible(driver, APP_LOGO).text
    assert titulo == "Products", f"Se esperaba 'Products' y se obtuvo '{titulo}'"
    assert logo == "Swag Labs", f"Se esperaba 'Swag Labs' y se obtuvo '{logo}'"


# ---------------------------------------------------------------------------
# 2. Navegación y verificación del catálogo
# ---------------------------------------------------------------------------
def test_catalogo_de_productos(driver_logueado):
    """Valida título, presencia de productos y elementos de la interfaz."""
    driver = driver_logueado

    # Título de la pestaña del navegador
    assert driver.title == "Swag Labs", f"Título incorrecto: '{driver.title}'"

    # Debe haber al menos un producto visible
    productos = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_all_elements_located(INVENTORY_ITEMS)
    )
    assert len(productos) > 0, "No se encontraron productos en el inventario"
    assert productos[0].is_displayed(), "El primer producto no es visible"

    # Elementos importantes de la interfaz: menú y filtro de orden
    assert esperar_visible(driver, MENU_BUTTON).is_displayed(), "Falta el botón de menú"
    assert esperar_visible(driver, SORT_DROPDOWN).is_displayed(), "Falta el filtro de orden"
    assert esperar_visible(driver, CART_LINK).is_displayed(), "Falta el ícono del carrito"

    # Nombre y precio del primer producto
    nombre = productos[0].find_element(*ITEM_NAME).text
    precio = productos[0].find_element(*ITEM_PRICE).text
    assert nombre != "", "El primer producto no tiene nombre"
    assert precio.startswith("$"), f"Precio con formato inesperado: '{precio}'"
    logger.info("Primer producto: %s - %s", nombre, precio)
    print(f"Primer producto: {nombre} - {precio}")


# ---------------------------------------------------------------------------
# 3. Interacción con productos (carrito)
# ---------------------------------------------------------------------------
def test_agregar_producto_al_carrito(driver_logueado):
    """Agrega el primer producto, verifica el contador y el contenido del carrito."""
    driver = driver_logueado

    # Datos del primer producto antes de agregarlo
    primer_producto = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_all_elements_located(INVENTORY_ITEMS)
    )[0]
    nombre_esperado = primer_producto.find_element(*ITEM_NAME).text

    # Click en "Add to cart" del primer producto
    primer_producto.find_element(*ADD_TO_CART_BUTTON).click()

    # El contador del carrito debe pasar a 1
    contador = esperar_visible(driver, CART_BADGE).text
    assert contador == "1", f"Contador del carrito esperado '1', obtenido '{contador}'"

    # Navegar al carrito
    esperar_clickeable(driver, CART_LINK).click()
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains(CART_URL_FRAGMENT))

    # El carrito debe tener exactamente 1 ítem con el nombre correcto
    items = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_all_elements_located(CART_ITEMS)
    )
    assert len(items) == 1, f"Se esperaba 1 ítem en el carrito y hay {len(items)}"
    nombre_en_carrito = items[0].find_element(By.CLASS_NAME, "inventory_item_name").text
    assert nombre_en_carrito == nombre_esperado, (
        f"En el carrito aparece '{nombre_en_carrito}' pero se agregó '{nombre_esperado}'"
    )
