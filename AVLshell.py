from collections import deque
import os


class AVLNode:
    should_show_tree = False

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1

    @staticmethod
    def find(root, val):
        if root is None:
            return False
        elif val == root.val:
            return True
        elif val < root.val:
            return AVLNode.find(root.left, val)
        else:
            return AVLNode.find(root.right, val)

    @staticmethod
    def insert(root, val):
        if root is None:
            root = AVLNode(val)
        elif val < root.val:
            root.left = AVLNode.insert(root.left, val)
        else:
            root.right = AVLNode.insert(root.right, val)

        AVLNode.update(root)
        return AVLNode.balance(root)

    @staticmethod
    def remove(root, val):
        if root is None:
            return None
        elif val < root.val:
            root.left = AVLNode.remove(root.left, val)
        elif val > root.val:
            root.right = AVLNode.remove(root.right, val)
        else:  # ==
            if root.left is None and root.right is None:
                return None
            elif root.left is None and root.right is not None:
                root = root.right
            elif root.left is not None and root.right is None:
                root = root.left
            elif root.left is not None and root.right is not None:
                new_root_to_be_removed = AVLNode.find_new_root(root.right)
                new_val = new_root_to_be_removed.val
                new_root = AVLNode(new_val)
                new_root.right = AVLNode.disconnect_new_root(
                    root.right, new_root_to_be_removed
                )
                new_root.left = root.left
                root = new_root
                AVLNode.should_show_tree = True

        AVLNode.update(root)
        return AVLNode.balance(root)

    @staticmethod
    def find_new_root(root):
        """pass .right"""
        while root.left is not None:
            root = root.left
        return root

    @staticmethod
    def disconnect_new_root(root, new_root):
        if root is new_root:
            return None
        root.left = AVLNode.disconnect_new_root(root.left, new_root)
        AVLNode.update(root)
        return root

    @staticmethod
    def update(root):
        root.height = 1 + max(
            AVLNode.get_height(root.left), AVLNode.get_height(root.right)
        )

    @staticmethod
    def balance(root):
        # print(val, balance, balance_left, balance_right)
        balance = AVLNode.get_balance(root)
        balance_left = AVLNode.get_balance(root.left)
        balance_right = AVLNode.get_balance(root.right)
        if abs(balance) > 1:
            if balance > 0 and balance_left >= 1:  # LL
                root = AVLNode.right_rotate(root)
            elif balance < 0 and balance_right <= -1:  # RR
                root = AVLNode.left_rotate(root)
            elif balance > 0 and balance_left <= -1:  # LR
                root.left = AVLNode.left_rotate(root.left)
                root = AVLNode.right_rotate(root)
            elif balance < 0 and balance_right >= 1:  # RL
                root.right = AVLNode.right_rotate(root.right)
                root = AVLNode.left_rotate(root)
            AVLNode.should_show_tree = True
        return root

    @staticmethod
    def left_rotate(node):
        r"""
          a
         / \
        d   b   
           / \
          e   c
          
          b
         / \
        a   c
       / \
      d   e   
        """

        a = node
        b = node.right
        e = b.left

        b.left = a
        a.right = e

        a.height = 1 + max(AVLNode.get_height(a.left), AVLNode.get_height(a.right))
        b.height = 1 + max(AVLNode.get_height(b.left), AVLNode.get_height(b.right))
        return b

    @staticmethod
    def right_rotate(node):
        # naopako od left_rotate
        a = node
        b = node.left
        e = b.right

        b.right = a
        a.left = e

        a.height = 1 + max(AVLNode.get_height(a.left), AVLNode.get_height(a.right))
        b.height = 1 + max(AVLNode.get_height(b.left), AVLNode.get_height(b.right))
        return b

    @staticmethod
    def get_balance(node):
        if node is None:
            return 0
        return AVLNode.get_height(node.left) - AVLNode.get_height(node.right)

    @staticmethod
    def get_height(node):
        if node is None:
            return 0
        return node.height

    @staticmethod
    def bfs_traversal(root):
        nodes = []
        q = deque()
        q.append(root)
        while len(q) != 0:
            node = q.popleft()
            if node is None:
                nodes.append(None)
            else:
                nodes.append(node.val)
                q.append(node.left)
                q.append(node.right)
        return nodes

    @staticmethod
    def display(node):
        if node is None:
            print("Stablo je prazno")
        else:
            lines, *_ = AVLNode._display_aux(node)
            for line in lines:
                print(line)

    def __contains__(self, x):
        return AVLNode.find(self, x)

    @staticmethod
    def _display_aux(node):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if node.right is None and node.left is None:
            line = "%s" % node.val
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if node.right is None:
            lines, n, p, x = AVLNode._display_aux(node.left)
            s = "%s" % node.val
            u = len(s)
            first_line = (x + 1) * " " + (n - x - 1) * "_" + s
            second_line = x * " " + "/" + (n - x - 1 + u) * " "
            shifted_lines = [line + u * " " for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if node.left is None:
            lines, n, p, x = AVLNode._display_aux(node.right)
            s = "%s" % node.val
            u = len(s)
            first_line = s + x * "_" + (n - x) * " "
            second_line = (u + x) * " " + "\\" + (n - x - 1) * " "
            shifted_lines = [u * " " + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = AVLNode._display_aux(node.left)
        right, m, q, y = AVLNode._display_aux(node.right)
        s = "%s" % node.val
        u = len(s)
        first_line = (x + 1) * " " + (n - x - 1) * "_" + s + y * "_" + (m - y) * " "
        second_line = (
            x * " " + "/" + (n - x - 1 + u + y) * " " + "\\" + (m - y - 1) * " "
        )
        if p < q:
            left += [n * " "] * (q - p)
        elif q < p:
            right += [m * " "] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * " " + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


def shell():
    root = None
    help = "komande: dodaj x, brisi x, izadji, prikazi, resetuj, pomoc"
    print(help)
    cmd = ""
    while True:
        cmd = input("> ").strip()
        op, *args = cmd.split(" ")
        arg = None
        if len(args) > 0:
            arg = int(args[0])

        if op == "izadji":
            exit()
        elif op == "prikazi":
            print(AVLNode.bfs_traversal(root))
            AVLNode.display(root)
        elif op == "dodaj":
            root = AVLNode.insert(root, arg)
        elif op == "brisi":
            root = AVLNode.remove(root, arg)
        elif op == "nadji":
            print("nadjen" if root is not None and arg in root else "nije nadjen")
        elif op == "resetuj":
            root = None
        elif op == "help" or op == "pomoc":
            print(help)
        else:
            print(f"{op} nije dozvoljena operacija (> pomoc)")

        if AVLNode.should_show_tree:
            AVLNode.display(root)
            AVLNode.should_show_tree = False


def main():
    shell()


if __name__ == "__main__":
    main()
