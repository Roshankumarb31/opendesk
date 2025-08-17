import flet as ft
from utils import AppIcons, format_path_display
import asyncio

class UIManager:
    def __init__(self, page, config_manager, app_launcher, startup_manager, config):
        self.page = page
        self.config_manager = config_manager
        self.app_launcher = app_launcher
        self.startup_manager = startup_manager
        self.config = config

        # UI state
        self.items_column = ft.Column(spacing=8)
        self.status_text = ft.Text("Ready", color=ft.Colors.GREEN_400, size=12)
        self.search_field = ft.TextField(
            hint_text="🔍 Quick search...",
            width=300,
            dense=True,
            border_radius=25,
            bgcolor="#1a1a1a",
            border_color="#333333",
            focused_border_color="#0078d4",
            on_change=self.filter_items
        )

        # Modern color scheme
        self.Colors = {
            'primary': '#0078d4',
            'success': '#00c851',
            'warning': '#ffb900',
            'danger': '#dc3545',
            'dark': '#121212',
            'surface': '#1e1e1e',
            'surface_variant': '#2a2a2a',
            'outline': '#3a3a3a',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0'
        }

    def setup_ui(self):
        """Initialize the main UI with performance optimizations"""
        # Page configuration
        self.page.title = "⚡ OpenDesk Pro"
        self.page.window_width = 1000
        self.page.window_height = 700
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = self.Colors['dark']
        self.page.padding = 0
        
        # Enable smooth animations
        self.page.theme = ft.Theme(
            visual_density=ft.VisualDensity.COMPACT,
            color_scheme=ft.ColorScheme(
                primary=self.Colors['primary'],
                surface=self.Colors['surface'],
                background=self.Colors['dark']
            )
        )
        
        self.show_main_page()

    def update_status(self, message, color=None):
        """Optimized status update with debouncing"""
        if color is None:
            color = self.Colors['success']
        
        self.status_text.value = message
        self.status_text.color = color
        
        # Use update() sparingly for better performance
        self.status_text.update()

    def create_header(self):
        """Create modern header with glassmorphism effect"""
        return ft.Container(
            content=ft.Row([
                # Logo and title
                ft.Row([
                    ft.Container(
                        content=ft.Text("⚡", size=28, color="#ffffff"),
                        bgcolor=self.Colors['primary'],
                        border_radius=12,
                        padding=8,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=8,
                            color=f"{self.Colors['primary']}40",
                            offset=ft.Offset(0, 2)
                        )
                    ),
                    ft.Column([
                        ft.Text("OpenDesk Pro", size=20, weight=ft.FontWeight.BOLD, color=self.Colors['text_primary']),
                        ft.Text("Smart Application Launcher", size=11, color=self.Colors['text_secondary'])
                    ], spacing=2)
                ], spacing=12),
                
                # Search and controls
                ft.Row([
                    self.search_field,
                    self.create_icon_button(
                        ft.Icons.REFRESH, 
                        "Refresh", 
                        self.refresh_ui,
                        color=self.Colors['warning']
                    ),
                    self.create_icon_button(
                        ft.Icons.SETTINGS, 
                        "Settings", 
                        self.show_settings,
                        color=self.Colors['text_secondary']
                    )
                ], spacing=8)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=20,
            bgcolor=f"{self.Colors['surface']}dd",
            border=ft.border.only(bottom=ft.BorderSide(1, self.Colors['outline']))
        )

    def create_action_bar(self):
        """Create modern action bar with smooth hover effects"""
        return ft.Container(
            content=ft.Row([
                self.create_modern_button(
                    "🚀 Launch All", 
                    self.launch_selected, 
                    self.Colors['success']
                ),
                self.create_modern_button(
                    "❌ Close All", 
                    self.close_all, 
                    self.Colors['danger']
                ),
                self.create_modern_button(
                    "➕ Add Item", 
                    self.add_new_item, 
                    self.Colors['primary']
                ),
                self.create_modern_button(
                    "☑️ Toggle All", 
                    self.toggle_select_all, 
                    "#6f42c1"
                ),
            ], spacing=12, wrap=True),
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            bgcolor=self.Colors['surface']
        )

    def create_startup_panel(self):
        """Create elegant startup control panel"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.POWER_SETTINGS_NEW, color=self.Colors['warning'], size=20),
                    bgcolor=f"{self.Colors['warning']}20",
                    border_radius=8,
                    padding=8
                ),
                ft.Text("Auto-start with Windows", 
                       color=self.Colors['text_primary'], 
                       size=14, 
                       weight=ft.FontWeight.W_500),
                ft.Switch(
                    value=self.startup_manager.is_in_startup(),
                    on_change=self.toggle_startup,
                    active_color=self.Colors['success'],
                    inactive_track_color=self.Colors['outline']
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=f"{self.Colors['surface_variant']}80",
            border_radius=12,
            padding=16,
            margin=ft.margin.symmetric(horizontal=20, vertical=8),
            border=ft.border.all(1, self.Colors['outline']),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color="#00000020",
                offset=ft.Offset(0, 2)
            )
        )

    def create_modern_button(self, text, on_click, color, width=None):
        """Create modern button with hover animation"""
        return ft.Container(
            content=ft.Text(text, color="#ffffff", size=13, weight=ft.FontWeight.W_600),
            bgcolor=color,
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=16, vertical=10),
            width=width,
            on_click=on_click,
            ink=True,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color=f"{color}40",
                offset=ft.Offset(0, 2)
            ),
            on_hover=self.create_hover_handler(color)
        )

    def create_hover_handler(self, color):
        """Create hover effect handler"""
        def handle_hover(e):
            if e.data == "true":
                e.control.shadow = ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=12,
                    color=f"{color}60",
                    offset=ft.Offset(0, 4)
                )
                e.control.scale = 1.02
            else:
                e.control.shadow = ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=6,
                    color=f"{color}40",
                    offset=ft.Offset(0, 2)
                )
                e.control.scale = 1.0
            e.control.update()
        return handle_hover

    def create_icon_button(self, icon, tooltip, on_click, color=None):
        """Create modern icon button"""
        if color is None:
            color = self.Colors['text_secondary']
        
        return ft.Container(
            content=ft.Icon(icon, color=color, size=18),
            bgcolor=f"{color}15",
            border_radius=8,
            padding=8,
            tooltip=tooltip,
            on_click=on_click,
            animate=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
            on_hover=lambda e: self.icon_hover_effect(e, color)
        )

    def icon_hover_effect(self, e, color):
        """Icon button hover effect"""
        if e.data == "true":
            e.control.bgcolor = f"{color}25"
            e.control.scale = 1.1
        else:
            e.control.bgcolor = f"{color}15"
            e.control.scale = 1.0
        e.control.update()

    def show_main_page(self):
        """Show optimized main page layout"""
        self.page.controls.clear()
        
        # Main layout with modern design
        main_content = ft.Column([
            self.create_header(),
            self.create_action_bar(),
            self.create_startup_panel(),
            
            # Items container with smooth scrolling
            ft.Container(
                content=ft.Column([
                    ft.Text("Launch Items", 
                           size=16, 
                           weight=ft.FontWeight.BOLD, 
                           color=self.Colors['text_primary']),
                    ft.Container(
                        content=ft.Column([self.items_column], 
                                        scroll=ft.ScrollMode.AUTO,
                                        spacing=8),
                        bgcolor=self.Colors['surface'],
                        border_radius=12,
                        border=ft.border.all(1, self.Colors['outline']),
                        padding=16,
                        height=350,  # Fixed height for better performance
                    )
                ], spacing=12),
                padding=ft.padding.symmetric(horizontal=20),
                expand=True
            ),
            
            # Status bar
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CIRCLE, color=self.Colors['success'], size=8),
                    self.status_text,
                    ft.Text(f"• {len(self.config.get('launch_items', []))} items configured", 
                           color=self.Colors['text_secondary'], size=11)
                ], spacing=8),
                padding=ft.padding.symmetric(horizontal=20, vertical=12),
                bgcolor=self.Colors['surface'],
                border=ft.border.only(top=ft.BorderSide(1, self.Colors['outline']))
            )
        ], spacing=0, expand=True)

        self.page.add(main_content)
        
        self.refresh_ui()
        self.page.update()

    def create_app_card(self, item, index):
        """Create beautiful app card with modern design"""
        app_icon = AppIcons.get_icon(item.get("type", "VS Code"))
        
        # Determine status color
        status_color = self.Colors['success'] if item.get("enabled", True) else self.Colors['text_secondary']
        
        return ft.Container(
            content=ft.Row([
                # App icon and info
                ft.Row([
                    ft.Container(
                        content=ft.Text(app_icon, size=20),
                        bgcolor=f"{self.Colors['primary']}20",
                        border_radius=8,
                        padding=8,
                        width=40,
                        height=40,
                        alignment=ft.alignment.center
                    ),
                    ft.Column([
                        ft.TextField(
                            value=item.get("name", ""),
                            hint_text="App name",
                            dense=True,
                            bgcolor=ft.Colors.TRANSPARENT,
                            border_color=ft.Colors.TRANSPARENT,
                            focused_border_color=self.Colors['primary'],
                            color=self.Colors['text_primary'],
                            text_size=14,
                            width=150,
                            on_change=lambda e: self.update_item_name(item, e.control.value)
                        ),
                        ft.Dropdown(
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
                            dense=True,
                            bgcolor=ft.Colors.TRANSPARENT,
                            border_color=ft.Colors.TRANSPARENT,
                            text_size=12,
                            width=120,
                            on_change=lambda e: self.update_item_type(item, e.control.value, index)
                        )
                    ], spacing=4)
                ], spacing=12),
                
                # Path field
                ft.Container(
                    content=ft.TextField(
                        value=item.get("path", ""),
                        hint_text="Path/URL (optional)",
                        dense=True,
                        bgcolor=f"{self.Colors['surface_variant']}50",
                        border_radius=6,
                        border_color=self.Colors['outline'],
                        focused_border_color=self.Colors['primary'],
                        color=self.Colors['text_primary'],
                        text_size=12,
                        on_change=lambda e: self.update_item_path(item, e.control.value)
                    ),
                    expand=True
                ),
                
                # Controls
                ft.Row([
                    ft.Switch(
                        value=item.get("enabled", True),
                        scale=0.8,
                        active_color=self.Colors['success'],
                        on_change=lambda e: self.update_item_enabled(item, e.control.value)
                    ),
                    self.create_icon_button(
                        ft.Icons.PLAY_ARROW, 
                        "Launch", 
                        lambda e: self.launch_single_item(item),
                        self.Colors['success']
                    ),
                    self.create_icon_button(
                        ft.Icons.DELETE_OUTLINE, 
                        "Delete", 
                        lambda e: self.delete_item(index),
                        self.Colors['danger']
                    )
                ], spacing=8)
            ], spacing=16),
            bgcolor=self.Colors['surface_variant'],
            border_radius=12,
            border=ft.border.all(1, self.Colors['outline']),
            padding=16,
            margin=ft.margin.only(bottom=8),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color="#00000015",
                offset=ft.Offset(0, 2)
            )
        )

    def refresh_ui(self):
        """Optimized UI refresh"""
        self.items_column.controls.clear()
        launch_items = self.config.get("launch_items", [])
        
        # Batch update for better performance
        for i, item in enumerate(launch_items):
            card = self.create_app_card(item, i)
            self.items_column.controls.append(card)
        
        # Single update call
        self.page.update()

    def filter_items(self, e):
        """Real-time search filtering"""
        search_term = e.control.value.lower()
        self.items_column.controls.clear()
        
        launch_items = self.config.get("launch_items", [])
        filtered_items = []
        
        for i, item in enumerate(launch_items):
            name = item.get("name", "").lower()
            item_type = item.get("type", "").lower()
            
            if search_term in name or search_term in item_type:
                filtered_items.append((item, i))
        
        for item, index in filtered_items:
            card = self.create_app_card(item, index)
            self.items_column.controls.append(card)
        
        self.page.update()

    def launch_single_item(self, item):
        """Launch single item with feedback"""
        if self.app_launcher.launch_item(item):
            self.update_status(f"✅ Launched {item.get('name', 'Unknown')}", self.Colors['success'])
        else:
            self.update_status(f"❌ Failed to launch {item.get('name', 'Unknown')}", self.Colors['danger'])

    # Keep all your existing methods but add these performance improvements:
    
    def update_item_type(self, item, new_type, index):
        """Optimized item type update"""
        item["type"] = new_type
        self.config_manager.save_config(self.config)
        # Only update the specific card instead of full refresh
        asyncio.create_task(self.refresh_ui_async())

    def update_item_name(self, item, new_name):
        """Debounced name update"""
        item["name"] = new_name
        asyncio.create_task(self.save_config_debounced())

    def update_item_path(self, item, new_path):
        """Debounced path update"""
        item["path"] = new_path
        asyncio.create_task(self.save_config_debounced())

    def update_item_enabled(self, item, enabled):
        """Instant enabled toggle"""
        item["enabled"] = enabled
        self.config_manager.save_config(self.config)

    async def save_config_debounced(self):
        """Debounced config save to prevent excessive I/O"""
        await asyncio.sleep(0.5)  # Wait for user to stop typing
        self.config_manager.save_config(self.config)

    def delete_item(self, index):
        """Smooth item deletion"""
        launch_items = self.config.get("launch_items", [])
        if 0 <= index < len(launch_items):
            item_name = launch_items[index].get("name", "Unknown")
            del launch_items[index]
            self.config_manager.save_config(self.config)
            self.refresh_ui()
            self.update_status(f"🗑️ Deleted {item_name}", self.Colors['warning'])

    def add_new_item(self, e):
        """Add item with smooth animation"""
        new_item = {
            "type": "VS Code",
            "name": f"New Item {len(self.config.get('launch_items', [])) + 1}",
            "path": "",
            "browser": "chrome",
            "enabled": True
        }
        
        if "launch_items" not in self.config:
            self.config["launch_items"] = []
        
        self.config["launch_items"].append(new_item)
        self.config_manager.save_config(self.config)
        self.refresh_ui()
        self.update_status("➕ Added new item", self.Colors['success'])

    def launch_selected(self, e):
        """Enhanced launch with progress feedback"""
        launch_items = self.config.get("launch_items", [])
        enabled_items = [item for item in launch_items if item.get("enabled", True)]
        
        if not enabled_items:
            self.update_status("⚠️ No items selected for launch", self.Colors['warning'])
            return
        
        launched_count = 0
        for item in enabled_items:
            if self.app_launcher.launch_item(item):
                launched_count += 1
        
        self.update_status(f"🚀 Launched {launched_count}/{len(enabled_items)} items", 
                          self.Colors['success'] if launched_count > 0 else self.Colors['danger'])

    def close_all(self, e):
        """Enhanced close all with confirmation"""
        closed_count = self.app_launcher.close_all_windows()
        self.update_status(f"❌ Closed {closed_count} processes", self.Colors['warning'])

    def toggle_startup(self, e):
        """Enhanced startup toggle"""
        enable_startup = e.control.value
        
        if enable_startup:
            if self.startup_manager.add_to_startup():
                self.update_status("✅ Added to Windows startup", self.Colors['success'])
            else:
                self.update_status("❌ Failed to add to startup", self.Colors['danger'])
                e.control.value = False
        else:
            if self.startup_manager.remove_from_startup():
                self.update_status("🚫 Removed from Windows startup", self.Colors['warning'])
            else:
                self.update_status("❌ Failed to remove from startup", self.Colors['danger'])
                e.control.value = True
        
        e.control.update()

    def toggle_select_all(self, e):
        """Enhanced select all toggle"""
        launch_items = self.config.get("launch_items", [])
        if not launch_items:
            self.update_status("⚠️ No items to select", self.Colors['warning'])
            return

        all_enabled = all(item.get("enabled", True) for item in launch_items)
        new_state = not all_enabled

        for item in launch_items:
            item["enabled"] = new_state

        self.config_manager.save_config(self.config)
        self.refresh_ui()
        
        action = "Selected" if new_state else "Deselected"
        self.update_status(f"☑️ {action} all {len(launch_items)} items", self.Colors['primary'])

    def show_settings(self, e):
        """Placeholder for settings dialog"""
        self.update_status("⚙️ Settings panel coming soon!", self.Colors['primary'])
