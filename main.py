from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Line
from random import uniform, choice


PINK = (1, 0.16, 0.45, 1)
LIGHT_PINK = (1, 0.72, 0.84, 1)
DARK = (0.015, 0.005, 0.012, 1)


class LoveCard(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.opacity = 0

        
        with self.canvas.before:
            Color(*DARK)
            self.background = RoundedRectangle(
                pos=self.pos,
                size=self.size
            )

        
        self.card = FloatLayout(
            size_hint=(None, None),
            size=(dp(330), dp(455)),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        with self.card.canvas.before:
            Color(0.035, 0.008, 0.025, 0.98)

            self.card_bg = RoundedRectangle(
                pos=self.card.pos,
                size=self.card.size,
                radius=[dp(25)]
            )

            Color(1, 0.12, 0.40, 0.8)

            self.card_border = Line(
                rounded_rectangle=(
                    self.card.x,
                    self.card.y,
                    self.card.width,
                    self.card.height,
                    dp(25)
                ),
                width=1.4
            )

        self.card.bind(pos=self.update_card, size=self.update_card)

        
        close = Label(
            text="×",
            font_size=dp(30),
            color=PINK,
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={"right": 1, "top": 1}
        )

        close.bind(on_touch_down=self.close_app)
        self.card.add_widget(close)

        
        self.heart = Label(
            text="♥",
            font_size=dp(90),
            color=PINK,
            size_hint=(1, None),
            height=dp(130),
            pos_hint={"center_x": 0.5, "top": 0.88}
        )

        self.card.add_widget(self.heart)

       
        title = Label(
            text="Love you, Iris",
            font_size=dp(30),
            bold=True,
            italic=True,
            color=LIGHT_PINK,
            size_hint=(1, None),
            height=dp(55),
            pos_hint={"center_x": 0.5, "top": 0.64}
        )

        self.card.add_widget(title)

        
        separator = Label(
            text="────────  ♥  ────────",
            font_size=dp(11),
            color=(1, 0.3, 0.55, 0.8),
            size_hint=(1, None),
            height=dp(30),
            pos_hint={"center_x": 0.5, "top": 0.54}
        )

        self.card.add_widget(separator)

        
        message = Label(
            text="Ты — самое прекрасное,\nчто произошло со мной.",
            font_size=dp(18),
            color=LIGHT_PINK,
            halign="center",
            valign="middle",
            size_hint=(0.9, None),
            height=dp(90),
            pos_hint={"center_x": 0.5, "top": 0.47}
        )

        message.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        self.card.add_widget(message)

        # Нижнее сердце
        bottom_heart = Label(
            text="♥",
            font_size=dp(42),
            color=PINK,
            size_hint=(1, None),
            height=dp(55),
            pos_hint={"center_x": 0.5, "y": 0.05}
        )

        self.card.add_widget(bottom_heart)

        self.add_widget(self.card)

        
        Clock.schedule_once(self.show_card, 0.2)

       
        Clock.schedule_once(self.animate_heart, 0.8)

       
        Clock.schedule_interval(self.spawn_heart, 0.5)

    def update_card(self, *args):
        self.card_bg.pos = self.card.pos
        self.card_bg.size = self.card.size

        self.card_border.rounded_rectangle = (
            self.card.x,
            self.card.y,
            self.card.width,
            self.card.height,
            dp(25)
        )

    def show_card(self, *args):
        Animation(
            opacity=1,
            duration=0.8,
            t="out_quad"
        ).start(self)

    def animate_heart(self, *args):

        animation = (
            Animation(
                font_size=dp(105),
                duration=0.6,
                t="out_quad"
            )
            + Animation(
                font_size=dp(90),
                duration=0.6,
                t="in_out_quad"
            )
        )

        animation.repeat = True
        animation.start(self.heart)

    def spawn_heart(self, *args):

        heart = Label(
            text=choice(["♥", "♡", "❤"]),
            font_size=dp(uniform(14, 25)),
            color=(1, 0.3, 0.6, uniform(0.4, 0.9)),
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            pos=(
                uniform(dp(15), dp(315)),
                dp(20)
            )
        )

        self.add_widget(heart)

        animation = Animation(
            y=dp(470),
            x=heart.x + uniform(-dp(40), dp(40)),
            opacity=0,
            duration=uniform(2.0, 3.0),
            t="out_quad"
        )

        animation.bind(
            on_complete=lambda *args:
            self.remove_widget(heart)
        )

        animation.start(heart)

    def close_app(self, widget, touch):

        if widget.collide_point(*touch.pos):
            Animation(
                opacity=0,
                duration=0.25
            ).start(self)

            Clock.schedule_once(
                lambda dt: App.get_running_app().stop(),
                0.3
            )

            return True


class LoveApp(App):

    title = "Love You, Iris"

    def build(self):

        Window.clearcolor = DARK

        root = FloatLayout()

        # Заставка
        splash = FloatLayout()

        splash_heart = Label(
            text="♥",
            font_size=dp(95),
            color=PINK,
            size_hint=(1, None),
            height=dp(120),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.56
            }
        )

        splash.add_widget(splash_heart)

        splash_title = Label(
            text="Love You, Iris",
            font_size=dp(29),
            bold=True,
            italic=True,
            color=LIGHT_PINK,
            size_hint=(1, None),
            height=dp(55),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.40
            }
        )

        splash.add_widget(splash_title)

        subtitle = Label(
            text="для тебя ❤️",
            font_size=dp(17),
            color=LIGHT_PINK,
            size_hint=(1, None),
            height=dp(35),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.33
            }
        )

        splash.add_widget(subtitle)

        root.add_widget(splash)

        
        animation = (
            Animation(
                font_size=dp(110),
                duration=0.55
            )
            + Animation(
                font_size=dp(95),
                duration=0.55
            )
        )

        animation.repeat = True
        animation.start(splash_heart)

       
        Clock.schedule_once(
            lambda dt: self.open_card(root, splash),
            1.7
        )

        return root

    def open_card(self, root, splash):

        root.remove_widget(splash)

        root.add_widget(
            LoveCard()
        )


if __name__ == "__main__":
    LoveApp().run()
