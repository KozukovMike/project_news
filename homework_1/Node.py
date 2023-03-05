from typing import Iterable, Optional, List


class Node:

    __number = 0
    all_objects = dict()

    def __init__(self,
                 values: Iterable,
                 parent: Optional["Node"] = None,
                 children: Optional[List["Node"]] = None
                 ):
        Node.__number += 1
        self.id = Node.__number
        self.values = values
        if isinstance(children, Iterable):
            self.children = []
            for child in children:
                if isinstance(child, Node):
                    if Node.all_objects[child.id].parent is None:
                        Node.all_objects[child.id].parent = self
                        self.children.append(child)
                    else:
                        raise ValueError('this Node already has a parent')
                else:
                    raise ValueError('this object is not a Node')
        elif isinstance(children, Node):
            if Node.all_objects[children.id].parent is None:
                self.children = []
                Node.all_objects[children.id].parent = self
                self.children.append(children)
            else:
                raise ValueError('this Node already has a parent')
        elif children is None:
            self.children = children
        else:
            raise ValueError('expected Optional[List["Node"]]')
        Node.all_objects[Node.__number] = self
        if isinstance(parent, Node):
            self.parent = parent
            if not Node.all_objects[parent.id].children:
                Node.all_objects[parent.id].children = [self]
            else:
                Node.all_objects[parent.id].children.append(self)
        elif parent is None:
            self.parent = parent
        else:
            raise ValueError('expected Node')

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


v = Node([1, 1])
a = Node([1, 2])
c = Node([1, 3], parent=a)
b = Node([1, 4], a)
print(a.children, b.children, c.children, c.parent)
