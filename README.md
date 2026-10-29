# QA Project — Urban Routes: UI Test Automation

Proyecto de automatización de pruebas end-to-end para Urban Routes, una aplicación de solicitud de taxis. Se automatizó el flujo completo de pedido de un servicio Comfort usando Selenium WebDriver con el patrón Page Object Model.

## Contexto

Urban Routes permite a los usuarios solicitar taxis configurando ruta, tarifa, método de pago y extras. El objetivo fue automatizar los 8 pasos del flujo de pedido, desde ingresar la dirección hasta confirmar que aparece el modal de estado del servicio.

## Casos de prueba automatizados (8)

| # | Caso | Verificación |
|---|------|--------------|
| 1 | Configurar ruta (origen y destino) | Los campos contienen los valores ingresados |
| 2 | Seleccionar tarifa Comfort | Click en tarjeta de tarifa |
| 3 | Ingresar número de teléfono y confirmar con SMS | Código SMS recuperado dinámicamente desde logs del navegador |
| 4 | Agregar tarjeta de crédito | Número de tarjeta + CVV con manejo de foco (TAB) |
| 5 | Dejar mensaje para el conductor | Campo de texto completado |
| 6 | Activar opción de manta y pañuelos | Switch activado |
| 7 | Solicitar 2 helados con contador de extras | Botón + presionado 2 veces |
| 8 | Confirmar el pedido y verificar modal | Modal de estado del pedido visible |

## Técnicas aplicadas

- **Page Object Model (POM)**: locators y métodos de interacción centralizados en `UrbanRoutesPage`
- **Esperas explícitas**: `WebDriverWait` para manejar elementos dinámicos y modales
- **Recuperación de código SMS**: lectura de logs de red del navegador vía `execute_cdp_cmd`
- **Manejo de focus**: uso de `Keys.TAB` para activar validaciones en campos de tarjeta

## Tecnologías

- Python 3.14
- Selenium WebDriver
- Pytest
- Page Object Model (POM)

## Estructura del proyecto

```
main.py    — Page Object (UrbanRoutesPage) + clase de pruebas (TestUrbanRoutes)
data.py    — datos de prueba separados del código de automatización
```

## Cómo ejecutar las pruebas

### Requisitos previos

- Python 3.x instalado
- Google Chrome instalado
- `chromedriver` compatible con tu versión de Chrome. Se recomienda usar [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) para instalarlo automáticamente:

```
pip install webdriver-manager
```

### Instalación y ejecución

1. Instalar dependencias:
```
pip install selenium pytest webdriver-manager
```
2. Configurar la URL de la aplicación en `data.py`
3. Ejecutar las pruebas:
```
pytest main.py -v
```
