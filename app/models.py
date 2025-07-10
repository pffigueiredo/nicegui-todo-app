from pydantic import BaseModel
from typing import List
from datetime import datetime


class TodoItem(BaseModel):
    id: int
    text: str
    completed: bool = False
    created_at: datetime = datetime.now()


class TodoList(BaseModel):
    items: List[TodoItem] = []
    next_id: int = 1
    
    def add_item(self, text: str) -> TodoItem:
        item = TodoItem(id=self.next_id, text=text)
        self.items.append(item)
        self.next_id += 1
        return item
    
    def toggle_item(self, item_id: int) -> None:
        for item in self.items:
            if item.id == item_id:
                item.completed = not item.completed
                break
    
    def delete_item(self, item_id: int) -> None:
        self.items = [item for item in self.items if item.id != item_id]
    
    def get_active_items(self) -> List[TodoItem]:
        return [item for item in self.items if not item.completed]
    
    def get_completed_items(self) -> List[TodoItem]:
        return [item for item in self.items if item.completed]