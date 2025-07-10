import pytest
from nicegui.testing import User
from nicegui import ui
from app.models import TodoList, TodoItem


async def test_todo_app_initial_state(user: User) -> None:
    """Test initial state of todo application"""
    await user.open('/')
    
    # Check if page elements are present
    await user.should_see('Todo Application')
    await user.should_see('Add new todo')
    await user.should_see('Total: 0 | Active: 0 | Completed: 0')
    await user.should_see('No todo items yet!')


async def test_add_todo_item(user: User) -> None:
    """Test adding a new todo item"""
    await user.open('/')
    
    # Add a todo item
    user.find(marker='todo-input').type('Buy groceries')
    user.find(marker='add-button').click()
    
    # Check if item was added
    await user.should_see('Buy groceries')
    await user.should_see('Total: 1 | Active: 1 | Completed: 0')
    await user.should_see('Active Items')


async def test_add_multiple_todo_items(user: User) -> None:
    """Test adding multiple todo items"""
    await user.open('/')
    
    # Add first todo
    user.find(marker='todo-input').type('First task')
    user.find(marker='add-button').click()
    
    # Add second todo
    user.find(marker='todo-input').type('Second task')
    user.find(marker='add-button').click()
    
    await user.should_see('First task')
    await user.should_see('Second task')
    await user.should_see('Total: 2 | Active: 2 | Completed: 0')


async def test_empty_todo_validation(user: User) -> None:
    """Test validation for empty todo items"""
    await user.open('/')
    
    # Try to add empty todo
    user.find(marker='add-button').click()
    
    # Should show warning and not add item
    await user.should_see('Total: 0 | Active: 0 | Completed: 0')


async def test_toggle_todo_completion(user: User) -> None:
    """Test toggling todo item completion"""
    await user.open('/')
    
    # Add a todo item
    user.find(marker='todo-input').type('Test todo')
    user.find(marker='add-button').click()
    
    # Toggle completion
    user.find(marker='checkbox-1').click()
    
    # Check if item moved to completed section
    await user.should_see('Completed Items')
    await user.should_see('Total: 1 | Active: 0 | Completed: 1')


async def test_delete_todo_item(user: User) -> None:
    """Test deleting a todo item"""
    await user.open('/')
    
    # Add a todo item
    user.find(marker='todo-input').type('Delete me')
    user.find(marker='add-button').click()
    
    # Delete the item
    user.find(marker='delete-1').click()
    
    # Check if item was deleted
    await user.should_see('Total: 0 | Active: 0 | Completed: 0')
    await user.should_see('No todo items yet!')


async def test_multiple_todo_items(user: User) -> None:
    """Test managing multiple todo items"""
    await user.open('/')
    
    # Add multiple items
    todos = ['First task', 'Second task', 'Third task']
    for todo in todos:
        user.find(marker='todo-input').type(todo)
        user.find(marker='add-button').click()
    
    # Check all items are present
    for todo in todos:
        await user.should_see(todo)
    
    await user.should_see('Total: 3 | Active: 3 | Completed: 0')
    
    # Complete one item
    user.find(marker='checkbox-1').click()
    
    await user.should_see('Total: 3 | Active: 2 | Completed: 1')
    await user.should_see('Active Items')
    await user.should_see('Completed Items')


class TestTodoModels:
    """Test the TodoList and TodoItem models"""
    
    def test_todo_item_creation(self):
        """Test creating a todo item"""
        item = TodoItem(id=1, text="Test todo")
        assert item.id == 1
        assert item.text == "Test todo"
        assert item.completed is False
        assert item.created_at is not None
    
    def test_todo_list_add_item(self):
        """Test adding items to todo list"""
        todo_list = TodoList()
        
        item1 = todo_list.add_item("First item")
        assert item1.id == 1
        assert item1.text == "First item"
        assert len(todo_list.items) == 1
        
        item2 = todo_list.add_item("Second item")
        assert item2.id == 2
        assert len(todo_list.items) == 2
    
    def test_todo_list_toggle_item(self):
        """Test toggling item completion"""
        todo_list = TodoList()
        item = todo_list.add_item("Test item")
        
        assert item.completed is False
        
        todo_list.toggle_item(item.id)
        assert item.completed is True
        
        todo_list.toggle_item(item.id)
        assert item.completed is False
    
    def test_todo_list_delete_item(self):
        """Test deleting items from todo list"""
        todo_list = TodoList()
        item1 = todo_list.add_item("First item")
        item2 = todo_list.add_item("Second item")
        
        assert len(todo_list.items) == 2
        
        todo_list.delete_item(item1.id)
        assert len(todo_list.items) == 1
        assert todo_list.items[0].id == item2.id
    
    def test_todo_list_filtering(self):
        """Test filtering active and completed items"""
        todo_list = TodoList()
        item1 = todo_list.add_item("Active item")
        item2 = todo_list.add_item("Completed item")
        
        todo_list.toggle_item(item2.id)  # Mark as completed
        
        active_items = todo_list.get_active_items()
        completed_items = todo_list.get_completed_items()
        
        assert len(active_items) == 1
        assert len(completed_items) == 1
        assert active_items[0].id == item1.id
        assert completed_items[0].id == item2.id