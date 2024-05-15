import flet as ft
import threading
import time
import random

class Actualizar:
    def __init__(self, campo1, campo2, contador, txt_number):
        self.campo1 = campo1
        self.campo2 = campo2
        self.contador = contador
        self.txt_number = txt_number
        self.ejecucion = False
        self.hilo = None

    def iniciar(self):
        if not self.ejecucion:
            self.ejecucion = True
            self.hilo = threading.Thread(target=self.actnumeros)
            self.hilo.start()

    def detener(self):
        self.ejecucion = False
        if self.hilo is not None:
            self.hilo.join()

    def actnumeros(self):
        while self.ejecucion:
            num1 = random.randint(10, 100)
            num2 = random.randint(10, 100)
            self.campo1.value = str(num1)
            self.campo2.value = str(num2)
            self.contador.page.update()

            tiempo_cambio = int(self.txt_number.value)

            for i in range(tiempo_cambio, -1, -1):
                if not self.ejecucion:
                    break
                self.contador.value = f"Cambio en: {i} segundos"
                self.contador.page.update()
                time.sleep(1)
            if not self.ejecucion:
                break

def main(page: ft.Page):
    page.title = "Flet: Contador"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="30", text_align="center", width=100)  

    def minus_click(e):
        current_value = int(txt_number.value)
        if current_value > 0:
            txt_number.value = str(current_value - 1)
            contador.value = f"Cambio en: {txt_number.value} segundos"
            page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        contador.value = f"Cambio en: {txt_number.value} segundos"
        page.update()

    txt_random1 = ft.TextField(value="", text_align="center", width=100)
    txt_random2 = ft.TextField(value="", text_align="center", width=100)
    contador = ft.Text(value="Cambio en: 30 segundos", text_align="center")  

    actualizador = Actualizar(txt_random1, txt_random2, contador, txt_number)

    def iniciar_actualizacion(e):
        actualizador.iniciar()

    def detener_actualizacion(e):
        actualizador.detener()

    page.add(
        ft.Column(
            [
                contador,
                ft.Row(
                    [
                        ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                        txt_number,
                        ft.IconButton(ft.icons.ADD, on_click=plus_click),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        txt_random1,
                        txt_random2,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.ElevatedButton("Iniciar", on_click=iniciar_actualizacion),
                        ft.ElevatedButton("Detener", on_click=detener_actualizacion),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
