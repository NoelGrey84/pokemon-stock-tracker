from src.discord_notifier import build_message
from src.models import ProductObservation,ProductStatus
def test_message(): 
 o=ProductObservation("Carrefour","Pokémon","https://carrefour.es/p",ProductStatus.IN_STOCK,price=29.99,purchase_online=True,pickup=True)
 m=build_message(o)
 assert "Carrefour" in m and "29,99 €" in m and "compra online" in m and "recogida" in m and o.url in m
