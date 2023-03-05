from typing import Iterable, Optional


class Node:

    __number = 0
    all_objects = dict()

    def __init__(self, values: Iterable, parent: Optional["Node"] = None):
        Node.__number += 1
        self.id = Node.__number
        self.values = values
        self.children = None
        self.parent = parent
        Node.all_objects[Node.__number] = self
        if parent and isinstance(parent, Node):
            self.parent = parent
            if not Node.all_objects[parent.id].children:
                Node.all_objects[parent.id].children = [self]
            else:
                Node.all_objects[parent.id].children.append(self)

    @staticmethod
    def get_by_id(id_):
        return Node.all_objects.get(id_)

    def is_root(self) -> bool:
        if self.parent:
            return True
        return False

    def is_leaf(self) -> bool:
        if self.children:
            return True
        return False


a = Node([1, 2])
b = Node([1, 2], a)
print(a.children, a.parent, b.children, b.parent)
