import pytest
from nicegui.testing import User


async def test_todo_persistence_workflow(user: User) -> None:
    """Test basic todo workflow and persistence"""
    await user.open('/')
    
    # Add some todos
    user.find(marker='todo-input').type('Buy milk')
    user.find(marker='add-button').click()
    
    user.find(marker='todo-input').type('Walk the dog')
    user.find(marker='add-button').click()
    
    # Check initial state
    await user.should_see('Total: 2 | Active: 2 | Completed: 0')
    await user.should_see('Buy milk')
    await user.should_see('Walk the dog')
    
    # Complete one task
    user.find(marker='checkbox-1').click()
    
    await user.should_see('Total: 2 | Active: 1 | Completed: 1')
    await user.should_see('Active Items')
    await user.should_see('Completed Items')
    
    # Delete one task
    user.find(marker='delete-2').click()
    
    await user.should_see('Total: 1 | Active: 0 | Completed: 1')


async def test_todo_edge_cases(user: User) -> None:
    """Test edge cases and error scenarios"""
    await user.open('/')
    
    # Test adding empty todo
    user.find(marker='add-button').click()
    await user.should_see('Total: 0 | Active: 0 | Completed: 0')
    
    # Test very long todo text
    long_todo = 'A' * 100
    user.find(marker='todo-input').type(long_todo)
    user.find(marker='add-button').click()
    
    await user.should_see('Total: 1 | Active: 1 | Completed: 0')
    
    # Test special characters in todo
    special_todo = 'Todo with special chars: @#$%^&*()'
    user.find(marker='todo-input').type(special_todo)
    user.find(marker='add-button').click()
    
    await user.should_see(special_todo)
    await user.should_see('Total: 2 | Active: 2 | Completed: 0')