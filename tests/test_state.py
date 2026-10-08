from src.state import StateStore
def test_transitions(tmp_path):
 s=StateStore(tmp_path/"state.json")
 assert not s.should_notify("x","OUT_OF_STOCK",set())
 s.update("x","OUT_OF_STOCK",set())
 assert s.should_notify("x","IN_STOCK",{"online"})
 s.update("x","IN_STOCK",{"online"})
 assert not s.should_notify("x","IN_STOCK",{"online"})
 assert s.should_notify("x","IN_STOCK",{"online","pickup"})
