from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle


class MegaSenaApp(App):
    def build(self):
        self.title = "Mega-Sena - Fechamento 12 Números"
        self.numeros_selecionados = []
        self.jogos_gerados = []
        self.botoes_60 = {}

        root = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(7))

        self.lbl_info = Label(
            text="Selecione 12 números de 01 a 60 (0/12)",
            size_hint_y=None, height=dp(42), bold=True, font_size=dp(16)
        )
        root.add_widget(self.lbl_info)

        scroll = ScrollView(size_hint_y=0.48, do_scroll_x=False)
        grid = GridLayout(cols=6, spacing=dp(5), padding=dp(3), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        for i in range(1, 61):
            btn = Button(text=f"{i:02d}", font_size=dp(14), size_hint_y=None, height=dp(44))
            btn.bind(on_release=lambda b, num=i: self.selecionar_numero(num))
            self.botoes_60[i] = btn
            grid.add_widget(btn)
        scroll.add_widget(grid)
        root.add_widget(scroll)

        root.add_widget(Label(text="12 Números Escolhidos:", bold=True,
                              size_hint_y=None, height=dp(28)))
        self.grid_12 = GridLayout(cols=6, rows=2, spacing=dp(4), size_hint_y=None, height=dp(76))
        self.labels_12 = []
        for _ in range(12):
            lbl = Label(text="-", bold=True, font_size=dp(15))
            self.labels_12.append(lbl)
            self.grid_12.add_widget(lbl)
        root.add_widget(self.grid_12)

        self.btn_gerar = Button(
            text="GERAR OS 6 JOGOS",
            disabled=True, size_hint_y=None, height=dp(48),
            background_color=(0.18, 0.49, 0.20, 1)
        )
        self.btn_gerar.bind(on_release=lambda *_: self.gerar_jogos())
        root.add_widget(self.btn_gerar)

        sorteio_box = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(5))
        sorteio_box.add_widget(Label(text="Sorteio:", size_hint_x=0.22, bold=True))
        self.ent_sorteio = TextInput(
            text="03, 12, 25, 34, 41, 58", multiline=False,
            input_filter=lambda text, from_undo: text
        )
        sorteio_box.add_widget(self.ent_sorteio)
        btn_conf = Button(text="CONFERIR", size_hint_x=0.30)
        btn_conf.bind(on_release=lambda *_: self.conferir())
        sorteio_box.add_widget(btn_conf)
        root.add_widget(sorteio_box)

        root.add_widget(Label(text="Jogos Gerados:", bold=True,
                              size_hint_y=None, height=dp(28)))
        games_scroll = ScrollView(size_hint_y=0.34, do_scroll_x=False)
        self.games_box = BoxLayout(orientation="vertical", spacing=dp(5), size_hint_y=None)
        self.games_box.bind(minimum_height=self.games_box.setter("height"))
        self.labels_jogos = []
        for i in range(6):
            lbl = Label(text=f"Jogo {i+1}: -", halign="left", valign="middle",
                        font_size=dp(14), size_hint_y=None, height=dp(38))
            lbl.bind(size=lambda inst, val: setattr(inst, "text_size", (inst.width, None)))
            self.labels_jogos.append(lbl)
            self.games_box.add_widget(lbl)
        games_scroll.add_widget(self.games_box)
        root.add_widget(games_scroll)

        return root

    def selecionar_numero(self, num):
        if num in self.numeros_selecionados:
            self.numeros_selecionados.remove(num)
            self.botoes_60[num].background_color = (1, 1, 1, 1)
        elif len(self.numeros_selecionados) < 12:
            self.numeros_selecionados.append(num)
            self.botoes_60[num].background_color = (0.35, 0.75, 0.40, 1)

        self.numeros_selecionados.sort()
        qtd = len(self.numeros_selecionados)
        self.lbl_info.text = f"Selecione 12 números de 01 a 60 ({qtd}/12)"
        for i, lbl in enumerate(self.labels_12):
            if i < qtd:
                lbl.text = f"{self.numeros_selecionados[i]:02d}"
            else:
                lbl.text = "-"
        self.btn_gerar.disabled = qtd != 12

    def gerar_jogos(self):
        N = self.numeros_selecionados
        indices_jogos = [
            [0, 1, 2, 3, 4, 5],
            [0, 1, 2, 6, 7, 8],
            [0, 3, 4, 6, 9, 10],
            [1, 5, 7, 8, 9, 11],
            [2, 3, 5, 7, 10, 11],
            [4, 6, 8, 9, 10, 11],
        ]
        self.jogos_gerados = [sorted(N[i] for i in indices) for indices in indices_jogos]
        for idx, jogo in enumerate(self.jogos_gerados):
            self.labels_jogos[idx].text = f"Jogo {idx+1}:  " + " - ".join(f"{n:02d}" for n in jogo)
            self.labels_jogos[idx].color = (0, 0, 0, 1)

    def conferir(self):
        if not self.jogos_gerados:
            self.aviso("Aviso", "Gere os 6 jogos antes de conferir.")
            return

        texto = self.ent_sorteio.text
        for sep in [",", "-", ";", "."]:
            texto = texto.replace(sep, " ")
        sorteados = set()
        for item in texto.split():
            if item.isdigit():
                val = int(item)
                if 1 <= val <= 60:
                    sorteados.add(val)

        if len(sorteados) != 6:
            self.aviso("Aviso", "Digite exatamente 6 números válidos (01 a 60).")
            return

        for idx, jogo in enumerate(self.jogos_gerados):
            acertos = len(set(jogo).intersection(sorteados))
            self.labels_jogos[idx].text = (
                f"Jogo {idx+1}:  " + " - ".join(f"{n:02d}" for n in jogo) +
                f"  [{acertos} acertos]"
            )
            self.labels_jogos[idx].color = (0.05, 0.45, 0.12, 1) if acertos >= 4 else (0, 0, 0, 1)

    def aviso(self, titulo, mensagem):
        Popup(title=titulo, content=Label(text=mensagem), size_hint=(0.85, 0.30)).open()


if __name__ == "__main__":
    MegaSenaApp().run()
