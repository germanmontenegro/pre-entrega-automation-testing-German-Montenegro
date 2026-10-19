# Pre-entrega: Automation Testing en saucedemo.com

## Propósito del proyecto
Automatizar con **Selenium WebDriver + Python + Pytest** los flujos básicos del sitio
de práctica [saucedemo.com](https://www.saucedemo.com):

1. **Login**: credenciales válidas (`standard_user` / `secret_sauce`), con espera explícita y
   validación de la URL `/inventory.html` y de los textos "Products" / "Swag Labs".
2. **Catálogo**: valida el título, la presencia de productos, el menú, el filtro de orden y
   muestra nombre y precio del primer producto.
3. **Carrito**: agrega el primer producto, verifica el contador del carrito, navega al carrito
   y comprueba que el producto agregado aparezca.

Los tests son **independientes**: cada uno abre su propio navegador.

## Tecnologías utilizadas
- Python 3.9+
- Selenium WebDriver 4 (el driver se descarga solo con Selenium Manager)
- Pytest y pytest-html
- Git y GitHub

## Estructura del proyecto
```
pre-entrega-automation-testing-German-Montenegro/
├── tests/
│   └── test_saucedemo.py   # Casos de prueba
├── utils/
│   └── helpers.py          # Driver, localizadores y funciones auxiliares
├── datos/                  # Datos externos (CSV/JSON), si se necesitaran
├── reports/                # Reporte HTML, log y capturas de pantalla
├── conftest.py             # Fixtures y captura automática en fallos
├── pytest.ini              # Configuración de pytest (reporte y logs)
├── requirements.txt
└── README.md
```

## Instalación de dependencias
Requiere tener Google Chrome instalado.

```bash
python -m venv venv
# Windows:  venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

## Cómo ejecutar las pruebas
```bash
pytest -v --html=reporte.html
```
También funciona simplemente con `pytest`: `pytest.ini` ya genera el reporte en
`reports/reporte.html` y el log en `reports/ejecucion.log`.

Para ejecutar sin abrir ventana de Chrome:
```bash
# Linux/Mac
HEADLESS=1 pytest
# Windows (PowerShell)
$env:HEADLESS=1; pytest
```

## Evidencias
- **Reporte HTML**: `reports/reporte.html`
- **Logs de ejecución**: `reports/ejecucion.log`
- **Capturas automáticas de fallos**: `reports/screenshots/`

## Autor
Nombre Apellido
