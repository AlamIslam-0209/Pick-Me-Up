import sys
from pathlib import Path



import StrukturData.Tower.Node as n

class Queue:
    def __init__(self):
        self.front = None 
        self.rear = None   
        self._size = 0

    def is_empty(self):
        return self.front is None

    def enqueue(self, data_hero):
        node_baru = n.Node(data_hero)
        
        if self.rear is None:
            self.front = self.rear = node_baru
            self._size += 1
            return
            
        self.rear.next = node_baru
        self.rear = node_baru
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            return "Antrean gacha kosong!"
            
        data_diklaim = self.front.data
        
        self.front = self.front.next
        self._size -= 1
        
        if self.front is None:
            self.rear = None
            
        return data_diklaim

    def front_item(self):
        """Melihat hero yang akan diklaim selanjutnya"""
        if self.is_empty():
            return "Antrean gacha kosong!"
        return self.front.data

    def size(self):
        return self._size
    