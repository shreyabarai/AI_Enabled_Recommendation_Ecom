import reflex as rx
import os
from groq import Groq
from dotenv import load_dotenv
from ..state.product_state import ProductState

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

class ChatState(rx.State):
    is_open: bool = False
    messages: list[dict[str, str]] = [{"role": "bot", "content": "Hi 👋 I'm your ShopHub AI assistant. How can I help you today?"}]
    input_text: str = ""
    is_typing: bool = False

    def toggle_chat(self):
        self.is_open = not self.is_open

    def clear_chat(self):
        """Reset the chat history."""
        self.messages = [{"role": "bot", "content": "Hi 👋 I'm your ShopHub AI assistant. How can I help you today?"}]
        self.input_text = ""
        self.is_typing = False

    async def send_message(self):
        if not self.input_text:
            return
        
        user_msg = self.input_text
        self.messages.append({"role": "user", "content": user_msg})
        self.input_text = ""
        self.is_typing = True
        yield

        try:
            # Get product context from ProductState
            product_state = await self.get_state(ProductState)
            
            # Ensure products are loaded
            if len(product_state.products) <= 1:
                product_state.load_products()
            
            available_products = product_state.products[:30]
            
            # Build context string
            product_list_str = ""
            for p in available_products:
                if p.get("id") != 0:
                    name = p.get("name", "Unknown")
                    pid = p.get("id", "")
                    cat = p.get("category", "")
                    price = p.get("price", "")
                    product_list_str += f"- {name} (ID: {pid}, Category: {cat}, Price: ₹{price})\n"
            
            system_prompt = f"""You are a helpful AI assistant for ShopHub, a premium e-commerce platform. 
Help users find products, answer questions about pricing, and provide recommendations.
Always provide product recommendations in a structured, point-wise format.
For each product you mention that exists in the list below, include a clickable link in markdown format: [Product Name](/product-details?id=ID).

Available Products Context:
{product_list_str}

Be concise, friendly, and professional."""

            # Call Groq API
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    *[{"role": m["role"] if m["role"] != "bot" else "assistant", "content": m["content"]} for m in self.messages]
                ],
            )
            bot_response = completion.choices[0].message.content
        except Exception as e:
            print(f"ERROR: Groq API call failed: {str(e)}")
            bot_response = "I'm sorry, I'm having trouble connecting to my brain right now. Please try again later."

        self.messages.append({"role": "bot", "content": bot_response})
        self.is_typing = False
        yield

def chatbot():
    return rx.box(
        # Chat Bubble
        rx.button(
            rx.icon(tag=rx.cond(ChatState.is_open, "x", "message-circle"), size=24),
            on_click=ChatState.toggle_chat,
            radius="full",
            size="4",
            bg="#10b981",
            color="white",
            box_shadow="0 10px 15px -3px rgba(16, 185, 129, 0.4)",
            _hover={"bg": "#059669", "transform": "scale(1.1)"},
            transition="all 0.2s",
            position="fixed",
            bottom="2rem",
            right="2rem",
            z_index="1000"
        ),
        # Chat Window
        rx.cond(
            ChatState.is_open,
            rx.vstack(
                rx.hstack(
                    rx.hstack(
                        rx.box(
                            rx.icon(tag="bot", size=20, color="white"),
                            padding="0.5rem",
                            bg="#059669",
                            border_radius="full"
                        ),
                        rx.vstack(
                            rx.text("ShopHub Assistant", size="3", weight="bold", color="white"),
                            rx.hstack(
                                rx.box(bg="#4ade80", width="8px", height="8px", border_radius="full"),
                                rx.text("Online", size="1", color="rgba(255,255,255,0.8)"),
                                align_items="center",
                                spacing="1"
                            ),
                            spacing="0"
                        ),
                        spacing="3",
                        align_items="center"
                    ),
                    rx.spacer(),
                    rx.hstack(
                        rx.icon_button(
                            rx.icon(tag="trash-2", size=18, color="white"),
                            variant="ghost",
                            on_click=ChatState.clear_chat,
                            _hover={"bg": "rgba(255,255,255,0.1)"}
                        ),
                        rx.icon_button(
                            rx.icon(tag="minus", size=18, color="white"),
                            variant="ghost",
                            on_click=ChatState.toggle_chat,
                            _hover={"bg": "rgba(255,255,255,0.1)"}
                        ),
                        spacing="2"
                    ),
                    width="100%",
                    bg="#10b981",
                    padding="1.5rem",
                    border_radius="1.5rem 1.5rem 0 0"
                ),
                rx.scroll_area(
                    rx.vstack(
                        rx.foreach(
                            ChatState.messages,
                            lambda msg: rx.box(
                                rx.vstack(
                                    rx.markdown(
                                        msg["content"]
                                    ),
                                    align_items=rx.cond(msg["role"] == "user", "end", "start"),
                                ),
                                padding="0.75rem 1rem",
                                border_radius="1.2rem",
                                bg=rx.cond(msg["role"] == "user", "#10b981", "#f3f4f6"),
                                color=rx.cond(msg["role"] == "user", "white", "#111827"),
                                align_self=rx.cond(msg["role"] == "user", "end", "start"),
                                max_width="85%",
                                box_shadow="0 1px 2px 0 rgba(0,0,0,0.05)"
                            )
                        ),
                        rx.cond(
                            ChatState.is_typing,
                            rx.hstack(
                                rx.text("Assistant is typing...", size="1", color="#6b7280"),
                                rx.spinner(size="1"),
                                spacing="2",
                                padding_left="1rem"
                            )
                        ),
                        spacing="4",
                        padding="1.5rem"
                    ),
                    height="400px",
                    width="100%",
                    bg="white"
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Type your message...",
                        value=ChatState.input_text,
                        on_change=ChatState.set_input_text,
                        variant="soft",
                        bg="#f9fafb",
                        border="1px solid #e5e7eb",
                        radius="full",
                        flex_grow="1",
                        padding_left="1rem"
                    ),
                    rx.icon_button(
                        rx.icon(tag="send", size=18),
                        on_click=ChatState.send_message,
                        bg="#10b981",
                        color="white",
                        radius="full",
                        _hover={"bg": "#059669"}
                    ),
                    padding="1rem 1.5rem",
                    width="100%",
                    bg="white",
                    border_top="1px solid #f3f4f6",
                    border_radius="0 0 1.5rem 1.5rem"
                ),
                width="380px",
                bg="white",
                border_radius="1.5rem",
                box_shadow="0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
                position="fixed",
                bottom="6rem",
                right="2rem",
                z_index="1000",
                spacing="0",
                transition="all 0.3s ease-in-out"
            )
        )
    )