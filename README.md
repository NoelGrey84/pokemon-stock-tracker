# Pokémon Stock Tracker

Rastreador personal de disponibilidad para **Pokémon 30.º Aniversario - Lote 6 Sobres** en El Corte Inglés, Hipercor y Carrefour. Solo comprueba páginas oficiales y envía avisos a Discord.

## No hace
No compra, reserva, añade al carrito, inicia sesión, usa credenciales, resuelve CAPTCHAs, evade anti-bot, rota IPs, usa proxies para evadir bloqueos ni accede a endpoints privados.

## Configuración
Copia `config.example.json` como `config.json` para ejecución local. Las URLs de producto son configurables y las de búsqueda son opcionales. Hipercor queda vacío hasta disponer de una ficha oficial fiable.

Variables de entorno/Secrets:
- `DISCORD_WEBHOOK_URL`: obligatorio para alertas.
- `STOCK_CONFIG_JSON`: opcional; JSON completo de configuración para GitHub Actions.

## GitHub Actions
`.github/workflows/stock-check.yml` ejecuta aproximadamente cada 5 minutos y también admite `workflow_dispatch`. GitHub no garantiza precisión exacta del cron.

El estado se guarda en `state.json` y solo cambia cuando cambia el estado/modalidad, evitando avisos repetidos. El workflow hace commit de ese archivo cuando cambia.

## Detección
Combina textos de compra/agotado/recogida/reserva con JSON-LD Schema.org y precio. HTTP 200 no implica stock. CAPTCHA/403/429/503 se marca como `BLOCKED` y se continúa con las demás tiendas.

Estados: `IN_STOCK`, `OUT_OF_STOCK`, `PICKUP_AVAILABLE`, `PREORDER`, `UNKNOWN`, `BLOCKED`.

## Pruebas
```bash
pip install -r requirements.txt
pytest -q
```
Los tests usan HTML fixtures y no dependen de las webs reales.

## URLs identificadas
El Corte Inglés: ficha oficial asociada al EAN 0196214145283.
Carrefour: ficha oficial asociada al EAN 0196214145283.
Hipercor: sin ficha fiable identificada; introducirla en `products.hipercor` cuando se confirme.

## Uso responsable
Mantén una petición por URL/tienda y respeta las condiciones y mecanismos técnicos de cada retailer.
