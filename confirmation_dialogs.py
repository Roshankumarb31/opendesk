import flet as ft

class ConfirmationPage:
    def __init__(self, page, ui_manager):
        self.page = page
        self.ui_manager = ui_manager
        
    def show_delete_confirmation(self):
        """Show delete all confirmation page"""
        self.page.controls.clear()
        
        main_content = ft.Column([
            ft.Container(height=100),  # Spacer
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.WARNING, size=80, color="#FF4B7A"),
                    ft.Text("Delete All Apps", size=24, weight=ft.FontWeight.BOLD, color="#ECECF1"),
                    ft.Text("Are you sure you want to delete all apps?", 
                           size=16, color="#8E93A8", text_align=ft.TextAlign.CENTER),
                    ft.Container(height=20),
                    ft.Row([
                        ft.ElevatedButton(
                            text="Cancel",
                            bgcolor="#464757",
                            color="#ffffff",
                            width=120,
                            on_click=lambda e: self.go_back()
                        ),
                        ft.ElevatedButton(
                            text="Delete All",
                            bgcolor="#FF4B7A",
                            color="#000000",
                            width=120,
                            on_click=lambda e: self.confirm_delete()
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=40,
                bgcolor="#21222A",
                border_radius=14,
                alignment=ft.alignment.center
            )
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.page.add(main_content)
        self.page.update()
    
    def show_close_confirmation(self):
        """Show close all confirmation page"""
        self.page.controls.clear()
        
        main_content = ft.Column([
            ft.Container(height=100),  # Spacer
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CLOSE, size=80, color="#FFD952"),
                    ft.Text("Close All Windows", size=24, weight=ft.FontWeight.BOLD, color="#ECECF1"),
                    ft.Text("Are you sure you want to close all windows/processes?", 
                           size=16, color="#8E93A8", text_align=ft.TextAlign.CENTER),
                    ft.Container(height=20),
                    ft.Row([
                        ft.ElevatedButton(
                            text="Cancel",
                            bgcolor="#464757",
                            color="#FFFFFF",
                            width=120,
                            on_click=lambda e: self.go_back()
                        ),
                        ft.ElevatedButton(
                            text="Close All",
                            bgcolor="#FFD952",
                            color="#000000",
                            width=120,
                            on_click=lambda e: self.confirm_close()
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=40,
                bgcolor="#21222A",
                border_radius=14,
                alignment=ft.alignment.center
            )
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.page.add(main_content)
        self.page.update()
    
    def go_back(self):
        """Return to main page"""
        self.ui_manager.show_main_page()
    
    def confirm_delete(self):
        """Execute delete and return to main"""
        self.ui_manager.show_main_page()
        self.ui_manager.delete_all(None)
    
    def confirm_close(self):
        """Execute close all and return to main"""
        self.ui_manager.show_main_page()
        self.ui_manager.close_all(None)
