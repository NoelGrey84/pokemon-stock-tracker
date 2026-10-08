from .base import StoreAdapter,parse_generic_product_page
class ElCorteInglesAdapter(StoreAdapter):
 name="El Corte Inglés"
 def parse(self,html,url): return parse_generic_product_page(html=html,url=url,store=self.name,product_name=self.product_name,rules={"out_of_stock":["agotado","no disponible"],"online":["comprar","añadir a la cesta","añadir a cesta","comprar ahora"],"pickup":["recogida en tienda","recoger en tienda","recogida"],"reservation":["reserva","reservar"],"preorder":["preventa","próximamente"]})
