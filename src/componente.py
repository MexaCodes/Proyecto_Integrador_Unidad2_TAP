import flet as ft

class ProductoCard(ft.Container):
    def __init__(self, producto_data, on_add_to_cart):
        super().__init__()
        self.data = producto_data  
        self.on_add_to_cart = on_add_to_cart
        # Quitamos width=250 para permitir que el grid defina el tamaño
        self.border_radius = 15
        self.bgcolor = ft.Colors.WHITE
        self.padding = 15
        self.shadow = ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12, offset=ft.Offset(0, 4))
        
        self.btn_fav = ft.IconButton(
            icon=ft.Icons.FAVORITE_BORDER, 
            icon_color=ft.Colors.RED_400,
            on_click=self.toggle_favorite
        )
        self.content = ft.Column(
            controls=[
                # Imagen que se adapta al ancho disponible
                ft.Image(src=self.data["img"], width=float("inf"), height=150, fit="contain"),
                ft.Text(self.data["nombre"], weight="bold", size=18, color=ft.Colors.BLACK),
                ft.Text(self.data["desc"], size=12, color=ft.Colors.GREY_700, max_lines=2),
                ft.Text(f"${self.data['precio']}", size=18, color=ft.Colors.GREEN, weight="w600"),
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        self.btn_fav,
                        ft.ElevatedButton(
                            content=ft.Row([ft.Icon(ft.Icons.ADD_SHOPPING_CART, size=20), ft.Text("Agregar")], tight=True),
                            on_click=lambda _: self.on_add_to_cart(self.data)
                        )
                    ]
                )
            ],
            tight=True
        )

    def toggle_favorite(self, e):
        self.btn_fav.icon = ft.Icons.FAVORITE if self.btn_fav.icon == ft.Icons.FAVORITE_BORDER else ft.Icons.FAVORITE_BORDER
        self.update()