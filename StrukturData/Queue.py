import StrukturData.Tower.Node as n

class Queue:
    def __init__(self):
        self.front = None 
        self.rear = None   
        self._size = 0

    def is_empty(self):
        """Memeriksa apakah antrean sedang kosong."""
        return self.front is None

    def enqueue(self, data):
        """Menambahkan data baru ke posisi paling belakang dari antrean."""
        node_baru = n.Node(data)
        
        if self.rear is None:
            self.front = self.rear = node_baru
            self._size += 1
            return
            
        self.rear.next = node_baru
        self.rear = node_baru
        self._size += 1

    def dequeue(self):
        """Mengambil data dari posisi paling depan dan mengeluarkannya dari antrean."""
        if self.is_empty():
            return "Antrean kosong!"
            
        pop = self.front.data
        
        self.front = self.front.next
        self._size -= 1
        
        if self.front is None:
            self.rear = None
            
        return pop

    def size(self):
        """
        Menghitung total jumlah data yang ada di dalam antrean.
        """
        return self._size
    

    