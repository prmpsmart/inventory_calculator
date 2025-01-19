import json
import os


class Item:
    def __init__(self, *, name: str, count: int, price: float) -> None:
        self.name = name
        self.count = count
        self.price = price


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
                items = load.get("items", [])

                if isinstance(items, list):
                    for item in items:
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

                        self.items.append(
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

    def add(
        self,
        *,
        name: str,
        count: int,
        price: float,
    ) -> Item:
        return self.add_item(
            Item(
                name=name,
                count=count,
                price=price,
            )
        )

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
                        items=self.items,
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
        self.history_file("w").writelines(self.history)

    def add_to_history(self, inventory: Inventory) -> None:
        if inventory.file and inventory.file not in self.history:
            self.history.append(inventory.file)
            self.save_history()

    def open_inventory(self, file: str) -> Inventory:
        return Inventory(file=file)

    def close_inventory(self, inventory: Inventory) -> Inventory:
        if inventory.save():
            self.add_to_history(inventory)


Inventories = Inventories()
