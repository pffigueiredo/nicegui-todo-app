from nicegui import ui, app
from app.models import TodoList, TodoItem


def create():
    @ui.page('/')
    def todo_page():
        # Initialize todo list in user storage
        if 'todo_list' not in app.storage.user:
            app.storage.user['todo_list'] = TodoList().dict()
        
        todo_list = TodoList(**app.storage.user['todo_list'])
        
        # Page title and styling
        ui.page_title('Todo Application')
        ui.add_head_html('''
        <style>
        .todo-container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .todo-item {
            display: flex;
            align-items: center;
            padding: 8px;
            margin: 4px 0;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            background: white;
        }
        .todo-item.completed {
            background: #f5f5f5;
            opacity: 0.7;
        }
        .todo-text {
            flex: 1;
            margin: 0 8px;
        }
        .todo-text.completed {
            text-decoration: line-through;
            color: #888;
        }
        .todo-header {
            text-align: center;
            margin-bottom: 30px;
        }
        .todo-input-section {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        .todo-input-section input {
            flex: 1;
        }
        .todo-stats {
            text-align: center;
            margin: 20px 0;
            color: #666;
        }
        </style>
        ''')
        
        with ui.column().classes('todo-container'):
            # Header
            with ui.row().classes('todo-header'):
                ui.label('📝 Todo Application').classes('text-2xl font-bold')
            
            # Input section
            with ui.row().classes('todo-input-section w-full'):
                new_todo_input = ui.input(
                    label='Add new todo',
                    placeholder='Enter your todo item...'
                ).classes('flex-1').mark('todo-input')
                
                add_button = ui.button(
                    'Add',
                    icon='add',
                    color='primary'
                ).classes('px-6').mark('add-button')
            
            # Stats section
            stats_label = ui.label().classes('todo-stats').mark('stats')
            
            # Todo list container
            todo_container = ui.column().classes('w-full').mark('todo-container')
            
            def update_display():
                """Update the todo list display"""
                todo_container.clear()
                
                active_items = todo_list.get_active_items()
                completed_items = todo_list.get_completed_items()
                
                # Update stats
                total_items = len(todo_list.items)
                active_count = len(active_items)
                completed_count = len(completed_items)
                
                stats_label.set_text(
                    f'Total: {total_items} | Active: {active_count} | Completed: {completed_count}'
                )
                
                with todo_container:
                    # Active items section
                    if active_items:
                        ui.label('📋 Active Items').classes('text-lg font-semibold mt-4 mb-2')
                        for item in active_items:
                            create_todo_item(item)
                    
                    # Completed items section
                    if completed_items:
                        ui.label('✅ Completed Items').classes('text-lg font-semibold mt-6 mb-2')
                        for item in completed_items:
                            create_todo_item(item)
                    
                    # Empty state
                    if not todo_list.items:
                        with ui.column().classes('text-center py-12'):
                            ui.label('🎯').classes('text-4xl mb-4')
                            ui.label('No todo items yet!').classes('text-xl text-gray-500')
                            ui.label('Add your first todo item above to get started.').classes('text-gray-400')
            
            def create_todo_item(item: TodoItem):
                """Create a todo item UI element"""
                with ui.row().classes('todo-item w-full' + (' completed' if item.completed else '')):
                    # Checkbox
                    ui.checkbox(
                        value=item.completed,
                        on_change=lambda e, item_id=item.id: toggle_todo(item_id)
                    ).mark(f'checkbox-{item.id}')
                    
                    # Todo text
                    text_classes = 'todo-text' + (' completed' if item.completed else '')
                    ui.label(item.text).classes(text_classes).mark(f'todo-text-{item.id}')
                    
                    # Delete button
                    ui.button(
                        icon='delete',
                        on_click=lambda e, item_id=item.id: delete_todo(item_id)
                    ).props('flat round color=red').classes('ml-2').mark(f'delete-{item.id}')
            
            def add_todo():
                """Add a new todo item"""
                text = new_todo_input.value.strip()
                if text:
                    todo_list.add_item(text)
                    new_todo_input.set_value('')
                    save_and_update()
                    ui.notify(f'Added: {text}', type='positive')
                else:
                    ui.notify('Please enter a todo item', type='warning')
            
            def toggle_todo(item_id: int):
                """Toggle completion status of a todo item"""
                todo_list.toggle_item(item_id)
                save_and_update()
                
                # Find the item to show notification
                for item in todo_list.items:
                    if item.id == item_id:
                        status = 'completed' if item.completed else 'reactivated'
                        ui.notify(f'Todo {status}!', type='info')
                        break
            
            def delete_todo(item_id: int):
                """Delete a todo item"""
                # Find the item text for notification
                item_text = None
                for item in todo_list.items:
                    if item.id == item_id:
                        item_text = item.text
                        break
                
                todo_list.delete_item(item_id)
                save_and_update()
                
                if item_text:
                    ui.notify(f'Deleted: {item_text}', type='warning')
            
            def save_and_update():
                """Save todo list to storage and update display"""
                app.storage.user['todo_list'] = todo_list.dict()
                update_display()
            
            def handle_enter(e):
                """Handle Enter key press in input field"""
                if e.key == 'Enter':
                    add_todo()
            
            # Event handlers
            add_button.on_click(add_todo)
            new_todo_input.on('keydown', handle_enter)
            
            # Initial display
            update_display()