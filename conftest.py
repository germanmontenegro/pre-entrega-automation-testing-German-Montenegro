"""
Configuración global de pytest.

- Fixture `driver`: un navegador nuevo por cada test (tests independientes).
- Fixture `driver_logueado`: driver con el login ya realizado.
- Hook que guarda una captura de pantalla automática cuando un test falla.
"""
import os
from datetime import datetime

import pytest

from utils.helpers import crear_driver, hacer_login

CARPETA_CAPTURAS = os.path.join("reports", "screenshots")


@pytest.fixture
def driver():
    """Crea un navegador limpio para cada test y lo cierra al terminar."""
    navegador = crear_driver()
    yield navegador
    navegador.quit()


@pytest.fixture
def driver_logueado(driver):
    """Devuelve un driver que ya inició sesión con standard_user."""
    hacer_login(driver)
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Si un test falla, guarda una captura de pantalla en reports/screenshots."""
    resultado = yield
    reporte = resultado.get_result()
    if reporte.when == "call" and reporte.failed:
        navegador = item.funcargs.get("driver")
        if navegador is not None:
            os.makedirs(CARPETA_CAPTURAS, exist_ok=True)
            marca = datetime.now().strftime("%Y%m%d_%H%M%S")
            ruta = os.path.join(CARPETA_CAPTURAS, f"{item.name}_{marca}.png")
            navegador.save_screenshot(ruta)
