class Node:
    def __init__(self, left=None, right=None, data=""):
        self.left = left
        self.right = right
        self.data = data
    
    def __str__(self):
        string = 'THIS: ' + self.data + '\n'
        string = string + 'Left: ' + self.left.data + '\n'
        if self.right:
            string = string + 'Right: ' + self.right.data + '\n'
        return string