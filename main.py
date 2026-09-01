from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.animation import Animation
from random import uniform, choice


class LoveWindow(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Dark background
        with self.canvas.before:
            Color(0.018, 0.008, 0.018, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[0])

        self.bind(size=self._update_bg, pos=self._update_bg)

        # Small centered "window"
        self.card = FloatLayout(
            size_hint=(None, None),
            size=(dp(330), dp(440)),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        with self.card.canvas.before:
            Color(0.035, 0.012, 0.035, 0.98)
            self.card_bg = RoundedRectangle(
                pos=self.card.pos,
                size=self.card.size,
                radius=[dp(22)]
            )
            Color(1, 0.25, 0.55, 0.9)
            self.card_border = Line(
                rounded_rectangle=(
                    self.card.x, self.card.y,
                    self.card.width, self.card.height, dp(22)
                ),
                width=dp(1.5)
            )

        self.card.bind(pos=self._update_card, size=self._update_card)

        # Close button
        close = Label(
            text="×",
            font_size=dp(30),
            color=(1, 0.55, 0.75, 1),
            size_hint=(None, None),
            size=(dp(45), dp(45)),
            pos_hint={"right": 1, "top": 1},
        )
        close.bind(on_touch_down=self.close_pressed)
        self.card.add_widget(close)

        # Heart
        self.heart = Label(
            text="♡",
            font_size=dp(92),
            color=(1, 0.25, 0.55, 1),
            size_hint=(1, None),
            height=dp(120),
            pos_hint={"center_x": 0.5, "top": 0.88},
        )
        self.card.add_widget(self.heart)

        # Title
        self.title = Label(
            text="Love you, Iris",
            font_size=dp(31),
            bold=True,
            italic=True,
            color=(1, 0.55, 0.75, 1),
            size_hint=(1, None),
            height=dp(55),
            pos_hint={"center_x": 0.5, "top": 0.63},
        )
        self.card.add_widget(self.title)

        # Divider
        divider = Label(
            text="────────  ♥  ────────",
            font_size=dp(12),
            color=(1, 0.35, 0.6, 0.7),
            size_hint=(1, None),
            height=dp(30),
            pos_hint={"center_x": 0.5, "top": 0.52},
        )
        self.card.add_widget(divider)

        # Message
        message = Label(
            text="Ты — самое прекрасное,\nчто произошло со мной. ❤️",
            font_size=dp(18),
            halign="center",
            valign="middle",
            color=(1, 0.78, 0.86, 1),
            size_hint=(0.9, None),
            height=dp(90),
            pos_hint={"center_x": 0.5, "top": 0.48},
        )
        message.bind(size=lambda obj, value: setattr(obj, "text_size", value))
        self.card.add_widget(message)

        # Bottom heart
        bottom_heart = Label(
            text="♥",
            font_size=dp(42),
            color=(1, 0.25, 0.55, 1),
            size_hint=(1, None),
            height=dp(55),
            pos_hint={"center_x": 0.5, "y": 0.05},
        )
        self.card.add_widget(bottom_heart)

        self.add_widget(self.card)

        # Heart animation
        Clock.schedule_once(self.start_animation, 0.8)
        Clock.schedule_interval(self.spawn_heart, 1.1)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def _update_card(self, *args):
        self.card_bg.pos = self.card.pos
        self.card_bg.size = self.card.size
        self.card_border.rounded_rectangle = (
            self.card.x, self.card.y,
            self.card.width, self.card.height, dp(22)
        )

    def start_animation(self, *args):
        anim = Animation(font_size=dp(105), duration=0.7) + Animation(
            font_size=dp(92), duration=0.7
        )
        anim.repeat = True
        anim.start(self.heart)

    def spawn_heart(self, *args):
        h = Label(
            text=choice(["♥", "♡", "❤"]),
            font_size=dp(uniform(14, 25)),
            color=(1, uniform(0.25, 0.7), uniform(0.5, 0.8), uniform(0.5, 0.9)),
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            pos=(self.card.x + uniform(dp(15), self.card.width-dp(35)),
                 self.card.y + dp(35)),
        )
        self.add_widget(h)
        target_y = self.card.top - dp(30)
        anim = Animation(
            y=target_y,
            x=h.x + uniform(-dp(35), dp(35)),
            opacity=0,
            duration=2.5
        )
        anim.bind(on_complete=lambda *x: self.remove_widget(h))
        anim.start(h)

    def close_pressed(self, widget, touch):
        if widget.collide_point(*touch.pos):
            App.get_running_app().stop()
            return True
        return False


class LoveYouIrisApp(App):
    title = "Love You, Iris"

    def build(self):
        Window.clearcolor = (0.018, 0.008, 0.018, 1)
        return LoveWindow()


if __name__ == "__main__":
    LoveYouIrisApp().run()
