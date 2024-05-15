import flet as ft
import threading
import time
import random

class ActualizadorNumerosAleatorios:
    def __init__(self, campo_texto1, campo_texto2, texto_contador):
        self.campo_texto1 = campo_texto1
        self.campo_texto2 = campo_texto2
        self.texto_contador = texto_contador
        self.en_ejecucion = False
        self.hilo = None

    def iniciar(self):
        if not self.en_ejecucion:
            self.en_ejecucion = True
            self.hilo = threading.Thread(target=self.actualizar_numeros)
            self.hilo.start()

    def detener(self):
        self.en_ejecucion = False
        if self.hilo is not None:
            self.hilo.join()

    def actualizar_numeros(self):
        while self.en_ejecucion:
            # Generar y mostrar números aleatorios inmediatamente
            num1 = random.randint(10, 100)
            num2 = random.randint(10, 100)
            self.campo_texto1.value = str(num1)
            self.campo_texto2.value = str(num2)
            self.texto_contador.page.update()
            
            # Esperar 30 segundos antes de la siguiente actualización
            for i in range(30, -1, -1):
                if not self.en_ejecucion:
                    break
                self.texto_contador.value = f"Próxima actualización en: {i} segundos"
                self.texto_contador.page.update()
                time.sleep(1)
            if not self.en_ejecucion:
                break

def main(page: ft.Page):
    page.title = "Flet: Contador y Números Aleatorios"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align="center", width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    txt_random1 = ft.TextField(value="", text_align="center", width=100)
    txt_random2 = ft.TextField(value="", text_align="center", width=100)
    texto_contador = ft.Text(value="Próxima actualización en: 30 segundos")

    actualizador = ActualizadorNumerosAleatorios(txt_random1, txt_random2, texto_contador)

    def iniciar_actualizacion(e):
        actualizador.iniciar()

    def detener_actualizacion(e):
        actualizador.detener()

    page.add(
        ft.Column(
            [
                texto_contador,
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
