from server.storage.indexes.bptree import BPlusTreeFile
from datetime import date
from server.types.datetime import DateType

ty = DateType(None)
bt = BPlusTreeFile("test.dat", ty)

bt.insert(DateType(date.fromisoformat("2025-06-20")), 0)
bt.insert(DateType(date.fromisoformat("2025-06-15")), 1)
bt.insert(DateType(date.fromisoformat("2025-06-18")), 2)
bt.insert(DateType(date.fromisoformat("2025-06-01")), 3)
bt.insert(DateType(date.fromisoformat("2025-06-04")), 4)
bt.insert(DateType(date.fromisoformat("2025-06-21")), 5)
bt.insert(DateType(date.fromisoformat("2025-06-12")), 6)
bt.insert(DateType(date.fromisoformat("2025-06-14")), 7)
bt.insert(DateType(date.fromisoformat("2025-06-16")), 8)
bt.insert(DateType(date.fromisoformat("2025-06-29")), 9)
bt.insert(DateType(date.fromisoformat("2025-06-27")), 10)
bt.insert(DateType(date.fromisoformat("2025-06-30")), 11)

#print(bt.search_record(DataType(9)))
for s in bt.get_all_records():
    print(s.key.value)

""" va = DateType(date.fromisoformat("2025-06-20")).serialize_to_bytes()
print(va)
print(DateType.deserialize_from_bytes(va).value) """