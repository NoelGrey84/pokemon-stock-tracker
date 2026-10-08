from .base import StoreAdapter,parse_generic_product_page
class CarrefourAdapter(StoreAdapter):
 name="Carrefour"
 def parse(self,html,url): return parse_generic_product_page(html=html,url=url,store=self.name,product_name=self.product_name,rules={"out_of_stock":["agotado temporalmente","agotado","no disponible"],"online":["añadir al carrito","añadir a la cesta","comprar","comprar ahora"],"pickup":["click&collect","recogida en tienda","recogida","recogida en un punto cercano"],"reservation":["reserva","reservar"],"preorder":["preventa","próximamente"]})
