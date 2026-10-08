from pathlib import Path
from src.stores.base import parse_generic_product_page
from src.models import ProductStatus
RULES={"out_of_stock":["agotado","no disponible"],"online":["añadir al carrito","comprar"],"pickup":["recogida en tienda"],"reservation":["reserva"],"preorder":["preventa"]}
def p(n):return Path("tests/fixtures",n).read_text(encoding="utf-8")
def parse(n):return parse_generic_product_page(html=p(n),url="https://example.test/product",store="Test",product_name="Pokémon",rules=RULES)
def test_out_of_stock():assert parse("out_of_stock.html").status==ProductStatus.OUT_OF_STOCK
def test_add_to_cart():o=parse("add_to_cart.html");assert o.status==ProductStatus.IN_STOCK and o.purchase_online
def test_pickup():assert parse("pickup.html").status==ProductStatus.PICKUP_AVAILABLE
def test_schema():o=parse("schema.html");assert o.status==ProductStatus.IN_STOCK and o.price==34.99
def test_unknown():assert parse_generic_product_page(html="<p>Producto</p>",url="x",store="T",product_name="P",rules=RULES).status==ProductStatus.UNKNOWN
