from StrukturData.Tower.Node import Node

class Stack:
    def __init__(self):
        self.top = None
        
    def push(self, data):
        """
        Menambahkan data baru ke tumpukan paling atas.
        """
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        
    def pop(self):
        """
        Mengambil dan mengeluarkan data dari tumpukan paling atas.
        """
        if self.is_empty():
            return None
        popped_data = self.top.data
        self.top = self.top.next
        return popped_data
    
    def peek(self):
        """
        Melihat data yang berada di tumpukan paling atas tanpa mengambilnya.
        """
        if self.is_empty():
            return None
        return self.top.data
    
    def is_empty(self):
        """
        Memeriksa apakah tumpukan data sudah kosong.
        """
        return self.top is None
    
    def size(self):
        """
        Menghitung jumlah data yang ada di dalam tumpukan saat ini.
        """
        count = 0
        current = self.top
        while current:
            count += 1
            current = current.next
        return count



