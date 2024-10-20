import mysql.connector




class Node:
    def __init__(self, username=None, password=None, id=None):
        self.username = username
        self.password = password
        self.left = None
        self.right = None
        self.id= id

def get_min_height_node(root, height=0):
    if root is None:
        return None, height
    left_height = get_height(root.left)
    right_height = get_height(root.right)
    if left_height == right_height:
        return root, height
    elif left_height < right_height:
        return get_min_height_node(root.left, height+1)
    else:
        return get_min_height_node(root.right, height+1)

def get_height(root):
    if root is None:
        return 0
    left_height = get_height(root.left)
    right_height = get_height(root.right)
    return max(left_height, right_height) + 1

def insert_node(root,new_id, username, password, pos_username=None):
    if pos_username is None or pos_username == '-1':
        node, height = get_min_height_node(root)
        if node is None:
            node = root
        print(f"Inserted node with username '{username}'")
    else:
        node = get_node_by_username(root, pos_username)
        if node is None:
            print(f"No node found with username '{pos_username}'. Node not inserted.")
            return root
        print(f"Inserted node with username '{username}' under node with username '{pos_username}'")

    new_node = Node(username, password, new_id)
    if node.left is None:
        node.left = new_node
    elif node.right is None:
        node.right = new_node
    else:
        # check if the left child has any children
        if node.left.left is None or node.left.right is None:
            insert_node(node.left, new_id, username, password)
        # if not, check if the right child has any children
        elif node.right.left is None or node.right.right is None:
            insert_node(node.right, new_id, username, password)
        # if both children have children, recursively call the function on the left child
        else:
            insert_node(node.left, new_id, username, password)

    return root


def get_node_by_username(root, username):
    if root is None:
        return None
    if root.username == username:
        return root
    node = get_node_by_username(root.left, username)
    if node is None:
        node = get_node_by_username(root.right, username)
    return node

def print_tree(root):
    def print_node(node, prefix='', is_left=True):
        if node is None:
            return
        print(f"{prefix}{'└── ' if is_left else '┌── '}{node.username}")
        print_node(node.left, f"{prefix}{'    ' if is_left else '│   '}", True)
        print_node(node.right, f"{prefix}{'│   ' if is_left else '    '}", False)

    print_node(root)
def print_tree(root, level=0):
    if root is not None:
        print_tree(root.right, level+1)
        print(" "*4*level + "->", root.username)
        print_tree(root.left, level+1)


def save_tree_to_db(root):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql237914!",
        database="BT"
    )
    cursor = db.cursor()
    db.commit()
    
    def traverse(node):
        if node is not None:
            cursor.execute("INSERT INTO binary_tree (id, username, password, left_child, right_child) VALUES (%s, %s, %s, %s, %s)", (node.id,node.username, node.password, None if node.left is None else node.left.id, None if node.right is None else node.right.id))
            db.commit()
            traverse(node.left)
            traverse(node.right)
            
    cursor.execute("TRUNCATE TABLE binary_tree")
    db.commit()
    traverse(root)
    db.close()

        
def load_tree_from_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql237914!",
        database="BT"
    )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM binary_tree ORDER BY id")
    rows = cursor.fetchall()
    node_map = {}
    if not rows:
        return None
    for row in rows:
        id, username, password, left_id, right_id = row
        node_map[id] = Node(username, password, id)
    for row in rows:
        id, username, password, left_id, right_id = row
        node = node_map[id]
        if left_id is not None:
            left_node = node_map[left_id]
            node.left = left_node
        if right_id is not None:
            right_node = node_map[right_id]
            node.right = right_node
    root_id = rows[0][0]
    root = node_map.get(root_id)
    db.close()
    return root



root = load_tree_from_db()
# get the maximum id value from the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="7861",
    database="web"
)
cursor = db.cursor()
cursor.execute("SELECT MAX(id) FROM binary_tree")
max_id = cursor.fetchone()[0]
db.close()
new_id = max_id if max_id is not None else 0  # assign a new id to the node




while True:
    choice = input("Enter '1' to insert a node, '2' to print the tree, or '3' to exit: ")
    if choice == '1':
        username = input("Enter username: ")
        if get_node_by_username(root, username) is not None:
            print(f"A node with username '{username}' already exists. Node not inserted.")
        else:
            new_id=new_id+1
            password = input("Enter password: ")
            pos_username = input("Enter the username of the node to insert under (optional, enter -1 to insert as child of min-height node): ")
            if root is None:
                root = Node(username, password,new_id)
                print(f"Inserted node with username '{username}' as the root node")
            else:
                insert_node(root, new_id, username, password, pos_username)
    elif choice == '2':
        if root is None:
            print("The tree is empty")
        else:
            print_tree(root)
    elif choice == '3':
        save_tree_to_db(root)
        break
    else:
        print("Invalid choice. Please try again.")






