import reflex as rx

class ThemeState(rx.State):
    dark_mode: bool = True

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode