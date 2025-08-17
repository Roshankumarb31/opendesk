import flet as ft
from utils import AppIcons, format_path_display

class UIManager:
    def __init__(self, page, config_manager, app_launcher, startup_manager, config):
        self.page = page
        self.config_manager = config_manager
        self.app_launcher = app_launcher
        self.startup_manager = startup_manager
        self.config = config

        # UI state
        self.items_column = ft.Column()
        self.status_text = ft.Text("Ready", color=ft.Colors.GREEN)

    def setup_ui(self):
        """Initialize the main UI"""
        self.page.title = "OpenDesk"
        self.page.window_width = 700
        self.page.window_height = 600
        self.page.theme_mode = ft.ThemeMode.DARK
        
        self.show_main_page()

    def update_status(self, message, color=ft.Colors.GREEN):
        """Update status text"""
        self.status_text.value = message
        self.status_text.color = color
        self.page.update()

    def show_main_page(self):
        """Show the main launcher page"""
        # Clear the page
        self.page.controls.clear()

        # Main layout
        self.page.add(
            ft.Container(
                content=ft.Column([
                    # Title
                    ft.Text("⚡ OpenDesk", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(),

                    # Control buttons
                    ft.Row([
                        ft.ElevatedButton("🚀 Launch Selected",
                                        on_click=self.launch_selected,
                                        bgcolor=ft.Colors.GREEN,
                                        color=ft.Colors.WHITE),
                        ft.ElevatedButton("❌ Close All",
                                        on_click=self.close_all,
                                        bgcolor=ft.Colors.RED,
                                        color=ft.Colors.WHITE),
                        ft.ElevatedButton("➕ Add New Item",
                                        on_click=self.add_new_item,
                                        bgcolor=ft.Colors.BLUE,
                                        color=ft.Colors.WHITE),
                        ft.ElevatedButton("☑️ Select All",
                                        on_click=self.toggle_select_all,
                                        bgcolor=ft.Colors.PURPLE,
                                        color=ft.Colors.WHITE),
                    ]),

                    # ADD THIS NEW SECTION - Startup Control
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.POWER_SETTINGS_NEW, 
                                color=ft.Colors.ORANGE, size=20),
                            ft.Text("Start with Windows:", 
                                color=ft.Colors.WHITE, size=14),
                            ft.Switch(
                                value=self.startup_manager.is_in_startup(),
                                on_change=self.toggle_startup,
                                active_color=ft.Colors.GREEN
                            )
                        ], spacing=10),
                        padding=ft.padding.symmetric(vertical=10),
                        bgcolor=ft.Colors.BLACK26,
                        border_radius=8,
                        margin=ft.margin.symmetric(vertical=5)
                    ),

                    ft.Divider(),

                    # Items section
                    ft.Text("Launch Items", size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Column([self.items_column], scroll=ft.ScrollMode.AUTO),
                        border=ft.border.all(1, ft.Colors.GREY),
                        padding=10,
                        border_radius=5,
                        height=400,
                    ),

                    # Status
                    ft.Row([
                        ft.Text("Status: "),
                        self.status_text
                    ])
                ]),
                padding=20
            )
        )

        # Initialize UI
        self.refresh_ui()
        self.page.update()


    def refresh_ui(self):
        """Refresh the UI with current data"""
        self.items_column.controls.clear()
        
        launch_items = self.config.get("launch_items", [])
        for i, item in enumerate(launch_items):
            self.items_column.controls.append(self.create_item_row(item, i))
        
        self.page.update()

    def create_item_row(self, item, index):
        """Create a row with dropdown, name field, path field, and browser dropdown"""
        # App type dropdown
        type_dropdown = ft.Dropdown(
            width=120,
            value=item.get("type", "VS Code"),
            options=[
                ft.dropdown.Option("VS Code"),
                ft.dropdown.Option("File Explorer"),
                ft.dropdown.Option("Command Prompt"),
                ft.dropdown.Option("PowerShell"),
                ft.dropdown.Option("Website"),
                ft.dropdown.Option("Teams"),
                ft.dropdown.Option("Outlook"),
                ft.dropdown.Option("MongoDB Compass"),
                ft.dropdown.Option("GitHub Desktop"),
                ft.dropdown.Option("Postman"),
                ft.dropdown.Option("Notepad"),
            ],
            on_change=lambda e: self.update_item_type(item, e.control.value, index)
        )

        # Name field
        name_field = ft.TextField(
            value=item.get("name", ""),
            hint_text="Item name",
            width=120,
            dense=True,
            on_change=lambda e: self.update_item_name(item, e.control.value)
        )

        # Path/URL field
        path_hint = "URL" if item.get("type") == "Website" else "Path (optional)"
        path_field = ft.TextField(
            value=item.get("path", ""),
            hint_text=path_hint,
            width=200,
            dense=True,
            on_change=lambda e: self.update_item_path(item, e.control.value)
        )

        # Enable checkbox
        enable_checkbox = ft.Checkbox(
            value=item.get("enabled", True),
            on_change=lambda e: self.update_item_enabled(item, e.control.value)
        )

        # Delete button
        delete_button = ft.IconButton(
            ft.Icons.DELETE,
            icon_color=ft.Colors.RED,
            on_click=lambda e: self.delete_item(index)
        )

        return ft.Row([
            enable_checkbox,
            type_dropdown,
            name_field,
            path_field,
            delete_button
        ])

    def update_item_type(self, item, new_type, index):
        """Update item type"""
        item["type"] = new_type
        self.config_manager.save_config(self.config)
        self.refresh_ui()

    def update_item_name(self, item, new_name):
        """Update item name"""
        item["name"] = new_name
        self.config_manager.save_config(self.config)

    def update_item_path(self, item, new_path):
        """Update item path"""
        item["path"] = new_path
        self.config_manager.save_config(self.config)

    def update_item_enabled(self, item, enabled):
        """Update item enabled status"""
        item["enabled"] = enabled
        self.config_manager.save_config(self.config)

    def delete_item(self, index):
        """Delete an item"""
        launch_items = self.config.get("launch_items", [])
        if 0 <= index < len(launch_items):
            del launch_items[index]
            self.config_manager.save_config(self.config)
            self.refresh_ui()

    def add_new_item(self, e):
        """Add a new launch item"""
        new_item = {
            "type": "VS Code",
            "name": "New Item",
            "path": "",
            "browser": "chrome",
            "enabled": True
        }
        
        if "launch_items" not in self.config:
            self.config["launch_items"] = []
            
        self.config["launch_items"].append(new_item)
        self.config_manager.save_config(self.config)
        self.refresh_ui()

    def launch_selected(self, e):
        """Launch all enabled items"""
        launched_count = 0
        launch_items = self.config.get("launch_items", [])
        
        for item in launch_items:
            if item.get("enabled", True):
                if self.app_launcher.launch_item(item):
                    launched_count += 1
        
        self.update_status(f"Launched {launched_count} items", ft.Colors.GREEN)

    def close_all(self, e):
        """Close all applications"""
        closed_count = self.app_launcher.close_all_windows()
        self.update_status(f"Closed {closed_count} processes", ft.Colors.ORANGE)



    def toggle_startup(self, e):
        """Toggle startup setting"""
        enable_startup = e.control.value
        
        if enable_startup:
            if self.startup_manager.add_to_startup():
                self.update_status("✅ Added to Windows startup", ft.Colors.GREEN)
            else:
                self.update_status("❌ Failed to add to startup", ft.Colors.RED)
                e.control.value = False  # Reset toggle
        else:
            if self.startup_manager.remove_from_startup():
                self.update_status("🚫 Removed from Windows startup", ft.Colors.ORANGE)
            else:
                self.update_status("❌ Failed to remove from startup", ft.Colors.RED)
                e.control.value = True  # Reset toggle
        
        self.page.update()

    def toggle_select_all(self, e):
        """Toggle between Select All and Deselect All"""
        launch_items = self.config.get("launch_items", [])
        if not launch_items:
            return

        # Check if all items are currently enabled
        all_enabled = all(item.get("enabled", True) for item in launch_items)
        new_state = not all_enabled

        # Update all items
        for item in launch_items:
            item["enabled"] = new_state

        # Update button text
        button_text = "☐ Deselect All" if new_state else "☑️ Select All"
        e.control.text = button_text

        # Save config and refresh UI
        self.config_manager.save_config(self.config)
        self.refresh_ui()

        # Update status
        action = "Selected" if new_state else "Deselected"
        count = len(launch_items)
        self.update_status(f"{action} all {count} items", ft.Colors.BLUE)
