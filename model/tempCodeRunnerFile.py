import mysql.connector 
try:
    con=mysql.connector.connect(host="hassu",
    user="root",password="7861",
            database="web")
            # for other queries
    con.autocommit=True
    cur=con.cursor(dictionary=True)
    print("successfull!") 
except:
        print("Error")

class Node:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.left = None
        self.right = None

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

def insert_node(root, username, password=None, pos_username=None):
    if get_node_by_username(root, username) is not None:
        print(f"A node with username '{username}' already exists. Node not inserted.")
        return root
    if pos_username is None or pos_username == '-1':
        node, height = get_min_height_node(root)
        if node is None:
            node = root
        print(f"Inserted node with username '{username}' at height '{height}'")
    else:
        node = get_node_by_username(root, pos_username)
        if node is None:
            print(f"No node found with username '{pos_username}'. Node not inserted.")
            return root
        print(f"Inserted node with username '{username}' under node with username '{pos_username}'")
    new_node = Node(username, password)
    if node.left is None:
        node.left = new_node
    elif node.right is None:
        node.right = new_node
    else:
        # check if the left child has any children
        if node.left.left is None or node.left.right is None:
            insert_node(node.left, username, password)
        # if not, check if the right child has any children
        elif node.right.left is None or node.right.right is None:
            insert_node(node.right, username, password)
        # if both children have children, recursively call the function on the left child
        else:
            insert_node(node.left, username, password)
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
def InsertInDB(root):
    if root is not None:
        InsertInDB(root.right)
        print("->",root.username)
        cur.execute(f"INSERT INTO nodes (node, pass) VALUES ('{root.username}', '{root.password}')")
        con.commit()
        print("successfull !")
        InsertInDB(root.left)
    

    con.close()


        


root = None
while True:
    choice = input("Enter '1' to insert a node, '2' to print the tree, or '3' to exit: ")
    if choice == '1':
        username = input("Enter username: ")
        password = input("Enter password: ")

        pos_username = input("Enter the username of the node to insert under (optional, enter -1 to insert as child of min-height node): ")
        if root is None:
            root = Node(username, password)
            print(f"root user and pass '{root.username}',   '{root.password}'")
            InsertInDB(root)
            print(f"Inserted node with username '{username}' as the root node")

            # InsertInDB(root)
        else:
            insert_node(root, username, password, pos_username)
            InsertInDB(root,username,password)
    elif choice == '2':
        if root is None:
            print("The tree is empty")
        else:
            print_tree(root)
    elif choice == '3':
        break
    else:
        print("Invalid choice. Please try again.")






