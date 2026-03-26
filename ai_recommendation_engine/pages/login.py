import reflex as rx

def login():
    return rx.hstack(

        rx.script("""
        if (!window.firebaseLoaded) {

        const script1 = document.createElement('script');
        script1.src = "https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js";
        document.head.appendChild(script1);

        const script2 = document.createElement('script');
        script2.src = "https://www.gstatic.com/firebasejs/8.10.1/firebase-auth.js";
        document.head.appendChild(script2);

        script2.onload = () => {

            // For Firebase JS SDK v7.20.0 and later, measurementId is optional
            const firebaseConfig = {
            apiKey: "AIzaSyCzOZMCq2nWDjIdbZv6e9p2yjZ3zXzlURQ",
            authDomain: "ai-recommendation-engine-sb.firebaseapp.com",
            projectId: "ai-recommendation-engine-sb",
            storageBucket: "ai-recommendation-engine-sb.firebasestorage.app",
            messagingSenderId: "546445701333",
            appId: "1:546445701333:web:e5051f73b9eba741fdf25c",
            measurementId: "G-MSWJGPWDFF"
            };

            firebase.initializeApp(firebaseConfig);

            // ✅ DEFINE FUNCTIONS AFTER LOAD
            window.loginUser = async function() {
                const email = document.getElementById("email").value;
                const password = document.getElementById("password").value;

                try {
                    await firebase.auth().signInWithEmailAndPassword(email, password);
                    alert("Login Success");
                    window.location.href = "/home";
                } catch (error) {
                    alert(error.message);
                }
            };

            window.signupUser = async function() {
                const email = document.getElementById("email").value;
                const password = document.getElementById("password").value;

                try {
                    await firebase.auth().createUserWithEmailAndPassword(email, password);
                    alert("Signup Success");
                } catch (error) {
                    alert(error.message);
                }
            };

            window.firebaseLoaded = true;
        };
        }
        """),
        
        # 🔵 LEFT SIDE
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text("✦", color="#34d399", font_size="1.5em"),
                    rx.text("ShopHub", font_weight="bold", font_size="1.2em"),
                ),

                rx.heading(
                    "Discover products you'll love.",
                    size="7"
                ),

                rx.text(
                    "AI-powered recommendations that learn your style. Join thousands of happy customers.",
                    color="gray"
                ),

                rx.hstack(
                    rx.vstack(rx.text("2M+"), rx.text("Users", color="gray")),
                    rx.vstack(rx.text("50K+"), rx.text("Products", color="gray")),
                    rx.vstack(rx.text("4.9★"), rx.text("Rating", color="gray")),
                    spacing="6"
                ),

                spacing="6",
                align="start"
            ),
            width="50%",
            height="100vh",
            padding="4em",
            color="white",
            background="radial-gradient(circle at top left, #0f172a, #020617)"
        ),

        # ⚪ RIGHT SIDE (FORM)
        rx.center(
            rx.box(
                rx.vstack(
                    rx.heading("Create account", size="6"),

                    rx.text("Start your personalized shopping journey", color="gray"),

                    # ✅ IMPORTANT: IDs added
                    rx.input(id="name", placeholder="Full Name", size="3"),
                    rx.input(id="email", placeholder="Email", size="3"),
                    rx.input(id="password", placeholder="Password", type="password", size="3"),

                    # 🔐 SIGNUP BUTTON
                    rx.button(
                        "Create Account →",
                        width="100%",
                        background="#10b981",
                        color="white",
                        _hover={"background": "#059669"},
                        on_click=rx.call_script("window.signupUser && window.signupUser()")
                    ),

                    # 🔐 LOGIN BUTTON
                    rx.button(
                        "Login",
                        width="100%",
                        variant="outline",
                        on_click=rx.call_script("window.loginUser && window.loginUser()")
                    ),

                    spacing="4",
                    width="300px"
                ),
                padding="2em"
            ),
            width="50%",
            height="100vh",
            background="white"
        ),
    )