import flet as ft
import subprocess
import json
import os
import psutil
import webbrowser
from pathlib import Path

class AppLauncher:
    def __init__(self):
        self.config_file = "launcher_config.json"
        self.apps_config = self.load_config()
        
    def load_config(self):
        """Load saved configuration from JSON file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "applications": [
                {"name": "VS Code", "command": "code", "type": "app", "enabled": True},
                {"name": "File Explorer", "command": "explorer", "type": "app", "enabled": True},
                {"name": "Command Prompt", "command": "cmd", "type": "app", "enabled": False},
                {"name": "PowerShell", "command": "powershell", "type": "app", "enabled": False},
            ],
            # ADD THIS NEW SECTION:
            "vscode_workspaces": [
                {"name": "Main Project", "path": "", "enabled": False},
                {"name": "Frontend", "path": "", "enabled": False},
                {"name": "Backend", "path": "", "enabled": False},
            ],
            "websites": [
                {"name": "GitHub", "url": "https://github.com", "browser": "chrome", "enabled": True},
                {"name": "Stack Overflow", "url": "https://stackoverflow.com", "browser": "edge", "enabled": False},
                {"name": "MDN Docs", "url": "https://developer.mozilla.org", "browser": "brave", "enabled": False},
            ]
    }

    def launch_vscode_workspace(self, workspace_config):
        """Launch VS Code with specific workspace/folder"""
        try:
            path = workspace_config["path"].strip()
            if path and os.path.exists(path):
                # Launch VS Code with the specific folder/workspace
                subprocess.Popen(["code", path], shell=True)
                return True
            elif not path:
                # Launch empty VS Code window
                subprocess.Popen(["code"], shell=True)
                return True
            else:
                print(f"Path does not exist: {path}")
                return False
        except Exception as e:
            print(f"Error launching VS Code for {workspace_config['name']}: {e}")
            return False

    def create_vscode_checkbox(workspace_config, index):
        """Create checkbox for VS Code workspace"""
        def on_change(e):
            workspace_config["enabled"] = e.control.value
            launcher.save_config()
        
        def on_path_change(e):
            workspace_config["path"] = e.control.value
            launcher.save_config()
        
        checkbox = ft.Checkbox(
            label=workspace_config["name"],
            value=workspace_config["enabled"],
            on_change=on_change
        )
        
        path_field = ft.TextField(
            value=workspace_config.get("path", ""),
            hint_text="Enter folder/workspace path",
            width=300,
            on_change=on_path_change,
            dense=True
        )
        
        return ft.Column([
            ft.Row([
                checkbox,
                ft.IconButton(
                    ft.Icons.FOLDER_OPEN,
                    tooltip="Browse folder"
                )
            ]),
            ft.Container(
                content=path_field,
                padding=ft.padding.only(left=40)
            )
        ])
    
    def add_new_vscode_workspace(e):
        """Add new VS Code workspace"""
        def save_new_workspace(e):
            if workspace_name.value:
                new_workspace = {
                    "name": workspace_name.value,
                    "path": workspace_path.value,
                    "enabled": True
                }
                launcher.apps_config["vscode_workspaces"].append(new_workspace)
                launcher.save_config()
                refresh_ui()
                page.dialog.open = False
                page.update()
        
        workspace_name = ft.TextField(label="Workspace Name", width=300)
        workspace_path = ft.TextField(label="Folder/Workspace Path", width=300)
        
        dialog = ft.AlertDialog(
            title=ft.Text("Add New VS Code Workspace"),
            content=ft.Column([
                workspace_name, 
                workspace_path,
                ft.Text("Examples:", size=12, color=ft.Colors.GREY),
                ft.Text("C:\\Projects\\MyApp", size=10, color=ft.Colors.GREY),
                ft.Text("D:\\Development\\Frontend", size=10, color=ft.Colors.GREY)
            ], height=200),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: close_dialog()),
                ft.TextButton("Add", on_click=save_new_workspace),
            ]
        )
        
        def close_dialog():
            page.dialog.open = False
            page.update()
        
        page.dialog = dialog
        dialog.open = True
        page.update()




    
    def save_config(self):
        """Save current configuration to JSON file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.apps_config, f, indent=2)
    
    def launch_application(self, app_config):
        """Launch a specific application"""
        try:
            if app_config["type"] == "app":
                subprocess.Popen(app_config["command"], shell=True)
            return True
        except Exception as e:
            print(f"Error launching {app_config['name']}: {e}")
            return False
    
    def launch_website(self, site_config):
        """Launch website in specified browser"""
        try:
            url = site_config["url"]
            browser = site_config["browser"].lower()
            
            browser_commands = {
                "chrome": "chrome",
                "edge": "msedge",
                "brave": "brave",
                "firefox": "firefox"
            }
            
            if browser in browser_commands:
                subprocess.Popen([browser_commands[browser], url])
            else:
                webbrowser.open(url)
            return True
        except Exception as e:
            print(f"Error opening {site_config['name']}: {e}")
            return False
    
    def close_all_windows(self):
        """Close all non-essential windows"""
        closed_count = 0
        
        # List of processes to close (add more as needed)
        target_processes = [
            "Code.exe", "explorer.exe", "cmd.exe", "powershell.exe",
            "chrome.exe", "msedge.exe", "brave.exe", "firefox.exe",
            "notepad.exe", "notepad++.exe"
        ]
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name']
                if proc_name in target_processes:
                    # Don't close the main explorer.exe (Windows shell)
                    if proc_name == "explorer.exe":
                        # Only close explorer windows, not the shell
                        if len(proc.children()) > 0:
                            proc.terminate()
                            closed_count += 1
                    else:
                        proc.terminate()
                        closed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return closed_count

def main(page: ft.Page):
    page.title = "Developer Launcher & Window Manager"
    page.window_width = 800
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.DARK
    
    launcher = AppLauncher()
    
    # Status text
    status_text = ft.Text("Ready", color=ft.Colors.GREEN)
    
    def update_status(message, color=ft.Colors.GREEN):
        status_text.value = message
        status_text.color = color
        page.update()
    
    def create_app_checkbox(app_config, index, is_website=False):
        """Create checkbox for application or website"""
        def on_change(e):
            app_config["enabled"] = e.control.value
            launcher.save_config()
        
        checkbox = ft.Checkbox(
            label=app_config["name"],
            value=app_config["enabled"],
            on_change=on_change
        )
        
        # Add browser info for websites
        if is_website:
            browser_dropdown = ft.Dropdown(
                width=100,
                value=app_config.get("browser", "chrome"),
                options=[
                    ft.dropdown.Option("chrome"),
                    ft.dropdown.Option("edge"),
                    ft.dropdown.Option("brave"),
                    ft.dropdown.Option("firefox"),
                ],
                on_change=lambda e: update_browser(app_config, e.control.value)
            )
            
            return ft.Row([
                checkbox,
                ft.Text(f"({app_config.get('url', '')})", size=10, color=ft.Colors.GREY),
                browser_dropdown
            ])
        else:
            return ft.Row([
                checkbox,
                ft.Text(f"({app_config.get('command', '')})", size=10, color=ft.Colors.GREY)
            ])
    
    def update_browser(app_config, browser):
        app_config["browser"] = browser
        launcher.save_config()
    
    def launch_selected(e):
        """Launch all selected applications, VS Code workspaces, and websites"""
        launched_count = 0
        
        # Launch applications
        for app in launcher.apps_config["applications"]:
            if app["enabled"]:
                if launcher.launch_application(app):
                    launched_count += 1
        
        # ADD THIS SECTION:
        # Launch VS Code workspaces
        for workspace in launcher.apps_config["vscode_workspaces"]:
            if workspace["enabled"]:
                if launcher.launch_vscode_workspace(workspace):
                    launched_count += 1
        
        # Launch websites
        for site in launcher.apps_config["websites"]:
            if site["enabled"]:
                if launcher.launch_website(site):
                    launched_count += 1
        
        update_status(f"Launched {launched_count} items", ft.Colors.GREEN)

    
    def close_all(e):
        """Close all windows"""
        closed_count = launcher.close_all_windows()
        update_status(f"Closed {closed_count} processes", ft.Colors.ORANGE)
    
    def add_new_app(e):
        """Add new application"""
        def save_new_app(e):
            if app_name.value and app_command.value:
                new_app = {
                    "name": app_name.value,
                    "command": app_command.value,
                    "type": "app",
                    "enabled": True
                }
                launcher.apps_config["applications"].append(new_app)
                launcher.save_config()
                refresh_ui()
                page.dialog.open = False
                page.update()
        
        app_name = ft.TextField(label="Application Name", width=300)
        app_command = ft.TextField(label="Command", width=300)
        
        dialog = ft.AlertDialog(
            title=ft.Text("Add New Application"),
            content=ft.Column([app_name, app_command], height=150),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: close_dialog()),
                ft.TextButton("Add", on_click=save_new_app),
            ]
        )
        
        def close_dialog():
            page.dialog.open = False
            page.update()
        
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    def add_new_website(e):
        """Add new website"""
        def save_new_website(e):
            if site_name.value and site_url.value:
                new_site = {
                    "name": site_name.value,
                    "url": site_url.value,
                    "browser": browser_choice.value,
                    "enabled": True
                }
                launcher.apps_config["websites"].append(new_site)
                launcher.save_config()
                refresh_ui()
                page.dialog.open = False
                page.update()
        
        site_name = ft.TextField(label="Website Name", width=300)
        site_url = ft.TextField(label="URL", width=300)
        browser_choice = ft.Dropdown(
            label="Browser",
            width=300,
            value="chrome",
            options=[
                ft.dropdown.Option("chrome"),
                ft.dropdown.Option("edge"),
                ft.dropdown.Option("brave"),
                ft.dropdown.Option("firefox"),
            ]
        )
        
        dialog = ft.AlertDialog(
            title=ft.Text("Add New Website"),
            content=ft.Column([site_name, site_url, browser_choice], height=200),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: close_dialog()),
                ft.TextButton("Add", on_click=save_new_website),
            ]
        )
        
        def close_dialog():
            page.dialog.open = False
            page.update()
        
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    def refresh_ui():
        """Refresh the UI with current configuration"""
        # Clear existing content
        apps_column.controls.clear()
        websites_column.controls.clear()
        
        # Add application checkboxes
        for i, app in enumerate(launcher.apps_config["applications"]):
            apps_column.controls.append(create_app_checkbox(app, i))
        
        # Add website checkboxes
        for i, site in enumerate(launcher.apps_config["websites"]):
            websites_column.controls.append(create_app_checkbox(site, i, is_website=True))
        
        page.update()
    
    # Create UI elements
    apps_column = ft.Column()
    websites_column = ft.Column()
    
    # Main layout
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("Developer Launcher & Window Manager", 
                       size=24, weight=ft.FontWeight.BOLD),
                
                ft.Divider(),
                
                # Control buttons
                ft.Row([
                    ft.ElevatedButton("🚀 Launch Selected", 
                                    on_click=launch_selected,
                                    bgcolor=ft.Colors.GREEN,
                                    color=ft.Colors.WHITE),
                    ft.ElevatedButton("❌ Close All Windows", 
                                    on_click=close_all,
                                    bgcolor=ft.Colors.RED,
                                    color=ft.Colors.WHITE),
                ]),
                
                ft.Divider(),
                
                # Applications section
                ft.Row([
                    ft.Text("Applications", size=18, weight=ft.FontWeight.BOLD),
                    ft.IconButton(ft.Icons.ADD, on_click=add_new_app, tooltip="Add Application"),
                ]),
                
                ft.Container(
                    content=ft.Column([apps_column]),
                    border=ft.border.all(1, ft.Colors.GREY),
                    padding=10,
                    border_radius=5,
                    height=200,
                ),
                
                # Websites section
                ft.Row([
                    ft.Text("Websites", size=18, weight=ft.FontWeight.BOLD),
                    ft.IconButton(ft.Icons.ADD, on_click=add_new_website, tooltip="Add Website"),
                ]),
                
                ft.Container(
                    content=ft.Column([websites_column]),
                    border=ft.border.all(1, ft.Colors.GREY),
                    padding=10,
                    border_radius=5,
                    height=200,
                ),
                
                ft.Divider(),
                
                # Status
                ft.Row([
                    ft.Text("Status: "),
                    status_text
                ])
            ]),
            padding=20
        )
    )
    
    # Initialize UI
    refresh_ui()

if __name__ == "__main__":
    ft.app(target=main)
