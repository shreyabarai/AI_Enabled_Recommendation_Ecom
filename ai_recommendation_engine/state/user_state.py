import reflex as rx

class UserState(rx.State):
    email: str = ""
    password: str = ""
    user_id: str = "guest_user"   # ✅ ADD THIS
    is_logged_in: bool = False

    def set_email(self, value: str):
        self.email = value

    def set_password(self, value: str):
        self.password = value

    def login(self):
        if self.email and self.password:
            self.is_logged_in = True
            self.user_id = self.email   # use email as ID
            return rx.redirect("/")
        else:
            return rx.window_alert("Invalid credentials")

    def signup(self):
        if self.email and self.password:
            return rx.window_alert("Signup successful! Please login.")
        else:
            return rx.window_alert("Please fill all fields")

    def logout(self):
        self.is_logged_in = False
        self.email = ""
        self.password = ""
        self.user_id = "guest_user"
        return rx.redirect("/login")