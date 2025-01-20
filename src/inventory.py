import json
import os
from typing import Optional


class Item:
    def __init__(self, *, name: str, count: int, price: float) -> None:
        self.name = name
        self.count = count
        self.price = price

    @property
    def amount(self) -> float:
        return self.count * self.price

    @classmethod
    def number_to_money(self, number: int | float) -> str:
        return f"{number:,}"

    @property
    def is_empty(self) -> bool:
        return not (self.name or self.count or self.price)

    @property
    def values(self) -> list[str]:
        return [
            self.name,
            self.number_to_money(self.count),
            self.number_to_money(self.price),
            self.number_to_money(self.amount),
        ]

    def __str__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


class Inventory:
    def __bool__(self):
        return True

    def __init__(
        self,
        name: str = "",
        items: list[Item] = [],
        file: str = "",
    ) -> None:
        self.file = file

        if file:
            if not os.path.isfile(file):
                open(file, "w")
            else:
                load = json.load(open(file))
                name = load.get("name", "")
                _items = load.get("items", [])

                items = []

                if isinstance(_items, list):
                    for item in _items:
                        item_name = item.get("name", "")
                        item_count = item.get("count", 0)
                        item_price = item.get("price", 0)

                        if not isinstance(item_name, str):
                            item_name = str(item_name)
                        if not isinstance(item_count, int):
                            try:
                                item_count = int(item_count)
                            except:
                                item_count = 0
                        if not isinstance(item_price, float):
                            try:
                                item_price = int(item_price)
                            except:
                                item_price = 0.0

                        items.append(
                            Item(
                                name=item_name,
                                count=item_count,
                                price=item_price,
                            )
                        )

        self.name = name
        self.items = items

    def add_item(self, item: Item) -> Item:
        self.items.append(item)
        return item

    def add(self, *, name: str = "", count: int = 0, price: float = 0.0) -> Item:
        return self.add_item(Item(name=name, count=count, price=price))

    def item(self, index: int) -> Optional[Item]:
        if index < len(self.items):
            return self.items[index]

    def item_values(self, index: int) -> list[str]:
        if item := self.item(index):
            return item.values
        return [""] * 4

    @property
    def total_amount(self) -> str:
        amount = sum([item.amount for item in self.items])
        return Item.number_to_money(amount)

    @property
    def total_items(self) -> int:
        return len(self.items)

    def insert_item(self, index: int, item: Item) -> None:
        if self.items:
            if len(self.items) > index:
                return self.items.insert(index, item)
        self.items.append(item)

    def remove_item(self, item: Item) -> None:
        if item in self.items:
            self.items.remove(item)

    def save(self, file: str = "") -> bool:
        self.file = file or self.file

        if self.file:
            try:
                json.dump(
                    dict(
                        name=self.name,
                        items=[item.__dict__ for item in self.items],
                    ),
                    open(self.file, "w"),
                )
                return True
            except Exception as e:
                print(e)
        return False

    @property
    def is_empty(self) -> bool:
        return not (self.name or self.file or self.items)


class Inventories:
    history_path = os.path.join(os.path.dirname(__file__), "history.txt")

    def __init__(self) -> None:
        self.history: list[str] = []

        if os.path.isfile(self.history_path):
            with self.history_file("r") as file:
                lines = file.readlines()

                for line in lines:
                    if (
                        (line := line.strip())
                        and os.path.splitext(line)[-1].lower() == ".json"
                        and os.path.isfile(line)
                    ):
                        self.history.append(line)

            self.save_history()

        else:
            self.history_file("w").close()

    def history_file(self, mode: str):
        return open(self.history_path, mode)

    def save_history(self):
        file = self.history_file("w")
        file.write('\n'.join(self.history))
        file.close()

    def add_to_history(self, inventory: Inventory) -> None:
        if inventory.file:
            if inventory.file in self.history:
                self.history.remove(inventory.file)

            self.history = [inventory.file] + self.history
            self.save_history()

    def open_inventory(self, file: str) -> Inventory:
        inventory = Inventory(file=file)
        self.add_to_history(inventory)
        return inventory

    def close_inventory(self, inventory: Inventory) -> Inventory:
        if inventory.save():
            self.add_to_history(inventory)


Inventories = Inventories()
