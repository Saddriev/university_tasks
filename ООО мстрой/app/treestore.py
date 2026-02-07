"""
Класс TreeStore: дерево объектов с полями id и parent.
Доступ по id и к детям за O(1), цепочка родителей за O(h).
"""
from typing import Any


class ItemNotFoundError(Exception):
    """Элемент с указанным id отсутствует в дереве."""

    def __init__(self, item_id: Any) -> None:
        self.item_id = item_id
        super().__init__(f"Item with id {item_id!r} not found")


class TreeStore:
    """
    Хранилище дерева с O(1) доступом к элементам по id и к детям по parent.
    При инициализации строятся индексы: по id, по дочерним, карта родителей.
    """

    def __init__(self, items: list[dict[str, Any]]) -> None:
        self._items = items
        self._items_by_id: dict[Any, dict[str, Any]] = {}
        self._children_by_id: dict[Any, list[dict[str, Any]]] = {}
        self._parent_map: dict[Any, Any] = {}
        self._root_id: Any = None
        self._build_indexes(items)

    def _build_indexes(self, items: list[dict[str, Any]]) -> None:
        """Строит индексы: по id, по дочерним элементам, карта родитель — id."""
        for item in items:
            item_id = item["id"]
            self._items_by_id[item_id] = item
            parent = item.get("parent")
            if parent != "root":
                self._parent_map[item_id] = parent
                if parent not in self._children_by_id:
                    self._children_by_id[parent] = []
                self._children_by_id[parent].append(item)
            else:
                self._parent_map[item_id] = None
                if self._root_id is None:
                    self._root_id = item_id

    def get_all(self) -> list[dict[str, Any]]:
        """Возвращает исходный массив элементов."""
        return self._items

    def get_item(self, item_id: Any) -> dict[str, Any]:
        """Возвращает элемент по id. ItemNotFoundError, если элемента нет."""
        item = self._items_by_id.get(item_id)
        if item is None:
            raise ItemNotFoundError(item_id)
        return item

    def get_children(self, item_id: Any) -> list[dict[str, Any]]:
        """Возвращает список дочерних элементов для данного id."""
        return self._children_by_id.get(item_id, [])

    def get_all_parents(self, item_id: Any) -> list[dict[str, Any]]:
        """Возвращает цепочку родителей от родителя элемента до корня."""
        result: list[dict[str, Any]] = []
        current_id = item_id
        while current_id is not None:
            item = self._items_by_id.get(current_id)
            if item is None:
                break
            if current_id != item_id:
                result.append(item)
            parent = self._parent_map.get(current_id)
            if parent == "root" and self._root_id is not None:
                root_item = self._items_by_id.get(self._root_id)
                if root_item:
                    result.append(root_item)
                break
            current_id = parent
        return result
