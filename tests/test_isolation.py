from types import SimpleNamespace
import src.main as main
from src.models import ProductObservation,ProductStatus
def test_store_isolation(monkeypatch):
 cfg=SimpleNamespace(product_name="Pokémon",postal_code="",city="")
 class Bad:
  name="Bad"
  def __init__(self,*a):pass
  def check(self,u):return ProductObservation(self.name,"P",u,ProductStatus.BLOCKED,error="403")
 class Good:
  name="Good"
  def __init__(self,*a):pass
  def check(self,u):return ProductObservation(self.name,"P",u,ProductStatus.OUT_OF_STOCK)
 monkeypatch.setitem(main.ADAPTERS,"bad",Bad);monkeypatch.setitem(main.ADAPTERS,"good",Good)
 assert main.check_store("bad",["https://example/b"],cfg)[0].status==ProductStatus.BLOCKED
 assert main.check_store("good",["https://example/g"],cfg)[0].status==ProductStatus.OUT_OF_STOCK
