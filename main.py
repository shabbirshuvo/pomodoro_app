import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color
from kivy.animation import Animation

kivy.require('2.0.0')


class BouncingBall(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (100, 100)
        with self.canvas:
            Color(1, 0, 0)  # Red color
            self.ellipse = Ellipse(pos=self.pos, size=self.size)
        self.anim = Animation(x=Window.width - self.width) + Animation(x=0)
        self.anim += Animation(y=Window.height - self.height) + Animation(y=0)
        self.anim.repeat = True
        self.anim.start(self)


class PomodoroApp(App):
    def build(self):
        # Set mobile-friendly window size
        Window.size = (360, 640)

        self.timer_seconds = 25 * 60  # 25 minutes
        self.timer_event = None

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Timer display
        self.timer_label = Label(text=self.format_timer(self.timer_seconds), font_size=30, size_hint_y=None, height=50)

        # Add start, stop, and reset buttons for the Pomodoro timer
        btn_layout = BoxLayout(size_hint_y=None, height=150)
        self.start_button = Button(text='Start', size_hint_x=0.33)
        self.start_button.bind(on_press=self.start_timer)

        self.stop_button = Button(text='Stop', size_hint_x=0.33)
        self.stop_button.bind(on_press=self.stop_timer)

        self.reset_button = Button(text='Reset', size_hint_x=0.33)
        self.reset_button.bind(on_press=self.reset_timer)

        btn_layout.add_widget(self.start_button)
        btn_layout.add_widget(self.stop_button)
        btn_layout.add_widget(self.reset_button)

        # Add bouncing balls
        self.balls = [BouncingBall() for _ in range(3)]
        for ball in self.balls:
            layout.add_widget(ball)

        layout.add_widget(self.timer_label)
        layout.add_widget(btn_layout)

        return layout

    def start_timer(self, instance):
        self.timer_event = Clock.schedule_interval(self.update_timer, 0.01)

    def stop_timer(self, instance):
        Clock.unschedule(self.timer_event)

    def reset_timer(self, instance):
        self.timer_seconds = 25 * 60
        self.timer_label.text = self.format_timer(self.timer_seconds)
        self.stop_timer(instance)

    def update_timer(self, dt):
        if self.timer_seconds > 0:
            self.timer_seconds -= 0.01
            self.timer_label.text = self.format_timer(self.timer_seconds)
        else:
            self.stop_timer(self.stop_button)

    def format_timer(self, seconds):
        mins, secs = divmod(int(seconds), 60)
        milsecs = int((seconds - int(seconds)) * 100)
        return f"{mins:02}:{secs:02}:{milsecs:02}"


if __name__ == '__main__':
    PomodoroApp().run()
