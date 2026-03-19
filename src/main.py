import flet as ft
from componente import ProductoCard 

def main(page: ft.Page):
    # --- CONFIGURACIÓN DE PÁGINA ---
    page.title = "Místico Tech - Tech Store"
    page.bgcolor = "#F0F2F5"
    page.theme_mode = ft.ThemeMode.LIGHT 
    
    # --- 1. BASE DE DATOS LOCAL ---
    productos_db = [
        {"id": 1, "nombre": "Laptop Gamer", "desc": "16GB RAM, RTX 3050", "precio": 22000, "img": "laptop.png"},
        {"id": 2, "nombre": "Mouse Pro", "desc": "Wireless, 12k DPI", "precio": 950, "img": "mouse.png"},
        {"id": 3, "nombre": "Teclado Mecánico", "desc": "RGB Blue Switches", "precio": 1800, "img": "teclado.png"},
        {"id": 4, "nombre": "Monitor LED", "desc": "24 pulg. Full HD", "precio": 3500, "img": "monitor.png"},
        {"id": 5, "nombre": "Audífonos Studio", "desc": "Noise Cancelling", "precio": 4200, "img": "audifinos.png"},
    ]
    
    carrito = []

    # --- 2. ELEMENTOS DE INTERFAZ ---
    catalogo_grid = ft.ResponsiveRow(spacing=20, run_spacing=20)
    lista_carrito_ui = ft.Column(scroll="auto", expand=True)
    texto_total = ft.Text("Total: $0", size=20, weight="bold", color=ft.Colors.GREEN_700)
    texto_contador = ft.Text("Carrito (0)", color=ft.Colors.WHITE, weight="bold")

    # --- 3. LÓGICA DEL CATÁLOGO ---
    def agregar_al_carrito(producto_data):
        carrito.append(producto_data)
        texto_contador.value = f"Carrito ({len(carrito)})"
        page.snack_bar = ft.SnackBar(ft.Text(f"{producto_data['nombre']} añadido!"), bgcolor="blue")
        page.snack_bar.open = True
        page.update()

    def refrescar_catalogo():
        catalogo_grid.controls.clear()
        for p in productos_db:
            # Aquí aplicamos la adaptabilidad: 1 col en móvil, 2 en tablet, 3 en PC
            catalogo_grid.controls.append(
                ft.Column([ProductoCard(p, agregar_al_carrito)], col={"xs": 12, "sm": 6, "md": 6, "lg": 4})
            )
        page.update()

    # --- 4. DIÁLOGO: AGREGAR NUEVO PRODUCTO ---
    nombre_input = ft.TextField(label="Nombre del Producto", border_color="blue")
    desc_input = ft.TextField(label="Descripción", border_color="blue", multiline=True)
    precio_input = ft.TextField(label="Precio", keyboard_type="number", border_color="blue")
    img_input = ft.TextField(label="Imagen (ej: disco.png)", value="monitor.png", border_color="blue")

    def guardar_nuevo_producto(e):
        if nombre_input.value and precio_input.value and desc_input.value:
            nuevo_p = {
                "id": len(productos_db) + 1,
                "nombre": nombre_input.value,
                "desc": desc_input.value,
                "precio": int(precio_input.value),
                "img": img_input.value
            }
            productos_db.append(nuevo_p)
            nombre_input.value = ""
            desc_input.value = ""
            precio_input.value = ""
            dialogo_nuevo.open = False
            refrescar_catalogo()
            page.update()

    dialogo_nuevo = ft.AlertDialog(
        title=ft.Text("Registrar Producto"),
        content=ft.Column([nombre_input, desc_input, precio_input, img_input], tight=True, width=400),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda _: (setattr(dialogo_nuevo, "open", False), page.update())),
            ft.ElevatedButton("Guardar", on_click=guardar_nuevo_producto)
        ]
    )
    page.overlay.append(dialogo_nuevo)

    def abrir_modal_registro(e):
        dialogo_nuevo.open = True
        page.update()

    # --- 5. PANEL CARRITO ---
    def realizar_pago(e):
        if not carrito: return
        total_pago = sum(item['precio'] for item in carrito)
        carrito.clear()
        texto_contador.value = "Carrito (0)"
        panel_carrito.visible = False
        page.snack_bar = ft.SnackBar(ft.Text(f"Pago exitoso por ${total_pago}"), bgcolor="green")
        page.snack_bar.open = True
        page.update()

    panel_carrito = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Tu Compra", size=24, weight="bold", color="black"),
                ft.IconButton(ft.Icons.CLOSE, icon_color="black", on_click=lambda _: (setattr(panel_carrito, "visible", False), page.update()))
            ], alignment="spaceBetween"),
            ft.Divider(),
            lista_carrito_ui,
            ft.Divider(),
            texto_total,
            ft.ElevatedButton("Finalizar Pago", bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE, width=300, on_click=realizar_pago)
        ]),
        bgcolor=ft.Colors.WHITE, padding=20, border_radius=20, visible=False, width=350, height=500,
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26),
    )

    def mostrar_carrito(e):
        lista_carrito_ui.controls.clear()
        for item in carrito:
            lista_carrito_ui.controls.append(
                ft.ListTile(title=ft.Text(item['nombre'], color="black"), subtitle=ft.Text(f"${item['precio']}", color="blue"))
            )
        texto_total.value = f"Total: ${sum(i['precio'] for i in carrito)}"
        panel_carrito.visible = True
        page.update()

    # --- 6. CABECERA (RESTAURADA) ---
    header = ft.Row(
        alignment="spaceBetween",
        controls=[
            ft.Text("Mistico Tech", size=30, weight="bold", color="black"),
            ft.Row([
                # AQUÍ ESTÁ TU BOTÓN DE AGREGAR PRODUCTOS
                ft.IconButton(ft.Icons.ADD_CIRCLE, icon_color="blue", icon_size=35, on_click=abrir_modal_registro),
                # AQUÍ ESTÁ TU BOTÓN DE COMPRAR / CARRITO
                ft.ElevatedButton(
                    content=ft.Row([ft.Icon(ft.Icons.SHOPPING_CART), texto_contador], tight=True),
                    on_click=mostrar_carrito, bgcolor=ft.Colors.BLUE_GREY_900
                )
            ])
        ]
    )

    refrescar_catalogo()

    # --- 7. ESTRUCTURA FINAL ---
    page.add(
        ft.Stack([
            ft.Container(content=ft.Column([header, ft.Divider(), catalogo_grid], scroll="auto"), padding=20),
            ft.Row([panel_carrito], alignment="end", vertical_alignment="start")
        ], expand=True)
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER)