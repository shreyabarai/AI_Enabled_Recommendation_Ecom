import reflex as rx
from ai_recommendation_engine.state.product_state import ProductState
from ai_recommendation_engine.components.product_card import product_card
from ai_recommendation_engine.components.navbar import navbar
from ai_recommendation_engine.components.footer import footer
from ai_recommendation_engine.components.chatbot import chatbot
from ai_recommendation_engine.components.cart_sidebar import cart_sidebar
from ai_recommendation_engine.state.cart_state import CartState

def categories_bar():
    return rx.hstack(
        rx.foreach(
            ProductState.categories,
            lambda cat: rx.button(
                cat,
                variant="ghost",
                color=rx.cond(ProductState.selected_category == cat, "#10b981", "#1f2937"),
                radius="full",
                bg=rx.cond(ProductState.selected_category == cat, "#f0fdf4", "transparent"),
                on_click=lambda: ProductState.set_category(cat),
                _hover={"bg": "#10b981", "color": "white"}
            )
        ),
        spacing="4",
        padding="0.5rem 4rem",
        bg="white",
        border_bottom="1px solid #f3f4f6"
    )

def stats_section():
    stats = [
        {"icon": "trending-up", "value": "2,400+", "label": "Products Trending"},
        {"icon": "package", "value": "18K", "label": "Orders Today"},
        {"icon": "clock", "value": "2.4 Days", "label": "Avg. Delivery"}
    ]
    return rx.hstack(
        rx.foreach(
            stats,
            lambda s: rx.hstack(
                rx.box(
                    rx.icon(tag=s["icon"], color="#10b981", size=24),
                    padding="1rem",
                    bg="#f0fdf4",
                    border_radius="1rem"
                ),
                rx.vstack(
                    rx.text(s["value"], weight="bold", size="5", color="#111827"),
                    rx.text(s["label"], color="#374151", size="2"),
                    spacing="0"
                ),
                spacing="3",
                align_items="center",
                bg="white",
                padding="1rem 2rem",
                border_radius="1.5rem",
                box_shadow="0 4px 6px -1px rgba(0,0,0,0.05)"
            )
        ),
        spacing="6",
        justify="center",
        margin_top="-2rem",
        z_index="10"
    )

def explore_categories():
    return rx.vstack(
        rx.heading("Explore Categories", size="7", weight="bold", color="#111827", margin_bottom="1.5rem"),
        rx.grid(
            rx.foreach(
                ProductState.categories,
                lambda cat: rx.vstack(
                    rx.box(
                        rx.icon(tag="layout-grid", color="#10b981", size=32),
                        padding="1.5rem",
                        bg=rx.cond(ProductState.selected_category == cat, "#f0fdf4", "white"),
                        border=rx.cond(ProductState.selected_category == cat, "2px solid #10b981", "1px solid #e5e7eb"),
                        border_radius="1.5rem",
                        box_shadow="0 1px 3px 0 rgba(0,0,0,0.1)",
                        on_click=lambda: ProductState.set_category(cat),
                        _hover={"transform": "translateY(-5px)", "transition": "all 0.3s"}
                    ),
                    rx.text(cat, size="2", weight="medium", color="#111827"),
                    spacing="2",
                    align_items="center",
                    cursor="pointer"
                )
            ),
            columns="8",
            spacing="6",
            width="100%"
        ),
        padding="4rem",
        align_items="start"
    )

def products_section():
    # Showing all products or filtered products
    return rx.vstack(
        rx.cond(
            ProductState.selected_category == "All",
            rx.heading("Our Products", size="7", weight="bold", color="#111827"),
            rx.heading(ProductState.selected_category, " Collection", size="7", weight="bold", color="#111827")
        ),
        rx.cond(
            ProductState.products.length() == 0,
            rx.center(
                rx.vstack(
                    rx.spinner(size="3"),
                    rx.text("Loading amazing products for you...", color="#374151"),
                    rx.button("Retry Loading", on_click=ProductState.load_products, variant="soft"),
                    spacing="4",
                    padding="4rem"
                ),
                width="100%"
            ),
            rx.grid(
                rx.foreach(ProductState.filtered_products, product_card),
                columns="4",
                spacing="6",
                width="100%",
                margin_top="2rem"
            )
        ),
        padding="4rem",
        align_items="start",
        width="100%"
    )

def recommended_section():
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading("✨ Picked for You", size="7", weight="bold", color="#111827"),
                rx.text("AI-curated recommendations based on your style", color="#374151"),
                align_items="start",
                spacing="1"
            ),
            rx.spacer(),
            rx.button("See all >", variant="ghost", color="#10b981"),
            width="100%",
            padding_right="1rem"
        ),
        rx.grid(
            rx.foreach(ProductState.recommended, product_card),
            columns="4",
            spacing="6",
            width="100%",
            margin_top="2rem"
        ),
        padding="0 4rem 4rem 4rem",
        align_items="start",
        width="100%"
    )

def hero_banner():
    return rx.box(
        rx.vstack(
            rx.heading("Summer Collection 2024", size="9", weight="bold", color="white"),
            rx.text("Discover the latest trends in fashion and electronics with AI-powered recommendations.", size="5", color="white", opacity=0.9),
            rx.hstack(
                rx.button("Shop Now", size="4", bg="#10b981", color="white", radius="full", _hover={"transform": "scale(1.05)"}),
                rx.button("Learn More", size="4", variant="outline", color="white", border="1px solid white", radius="full"),
                spacing="4",
                margin_top="2rem"
            ),
            align_items="start",
            justify_content="center",
            height="400px",
            padding="4rem"
        ),
        background="linear-gradient(to right, rgba(0,0,0,0.7), rgba(0,0,0,0.3)), url('https://images.unsplash.com/photo-1441986300917-64674bd600d8?q=80&w=2070&auto=format&fit=crop')",
        background_size="cover",
        background_position="center",
        border_radius="2rem",
        margin="2rem 4rem",
        overflow="hidden"
    )

def section_header(title, subtitle=None):
    return rx.vstack(
        rx.hstack(
            rx.heading(title, size="7", weight="bold", color="#111827"),
            rx.spacer(),
            rx.button("View All", variant="ghost", color="#10b981", _hover={"bg": "#f0fdf4"}),
            width="100%",
            align_items="center"
        ),
        rx.cond(
            subtitle,
            rx.text(subtitle, color="#374151", size="3"),
        ),
        width="100%",
        spacing="1",
        margin_bottom="2rem"
    )

def home():
    return rx.box(
        navbar(),
        rx.vstack(
            categories_bar(),
            hero_banner(),
            
            # Search Results Section (Conditional)
            rx.cond(
                ProductState.search_query,
                rx.vstack(
                    section_header(f"Search Results for '{ProductState.search_query}'"),
                    rx.cond(
                        ProductState.filtered_products.length() == 0,
                        rx.center(
                            rx.vstack(
                                rx.icon(tag="search-x", size=48, color="#9ca3af"),
                                rx.text(f"No products found for '{ProductState.search_query}'", color="#374151", size="4"),
                                rx.button("Clear Search", on_click=lambda: ProductState.set_search_query(""), variant="soft"),
                                spacing="4",
                                padding="4rem"
                            ),
                            width="100%"
                        ),
                        rx.grid(
                            rx.foreach(ProductState.filtered_products, product_card),
                            columns="4",
                            spacing="6",
                            width="100%"
                        )
                    ),
                    padding="4rem",
                    width="100%",
                    bg="#f0fdf4"  # Light green background to highlight search results
                )
            ),

            # Popular Products Section
            rx.cond(
                ~ProductState.search_query,
                rx.vstack(
                    section_header("Popular Products", "Most loved items by our community"),
                    rx.grid(
                        rx.foreach(ProductState.popular, product_card),
                        columns="4",
                        spacing="6",
                        width="100%"
                    ),
                    padding="4rem",
                    width="100%"
                )
            ),

            # Recommendations Section
            rx.cond(
                ~ProductState.search_query,
                rx.vstack(
                    section_header("Recommended for You", "AI-curated picks based on your style"),
                    rx.grid(
                        rx.foreach(ProductState.recommended, product_card),
                        columns="4",
                        spacing="6",
                        width="100%"
                    ),
                    rx.center(
                        rx.button(
                            "Generate New Recommendations",
                            on_click=ProductState.load_products, # For now, re-randomize
                            size="4",
                            bg="#10b981",
                            color="white",
                            radius="full",
                            margin_top="3rem",
                            _hover={"transform": "scale(1.05)"}
                        ),
                        width="100%"
                    ),
                    padding="0 4rem 4rem 4rem",
                    width="100%"
                )
            ),
            
            # All Products Section (if no category selected)
            rx.cond(
                (ProductState.selected_category == "All") & (~ProductState.search_query),
                rx.vstack(
                    section_header("All Products"),
                    rx.grid(
                        rx.foreach(ProductState.filtered_products, product_card),
                        columns="4",
                        spacing="6",
                        width="100%"
                    ),
                    padding="0 4rem 4rem 4rem",
                    width="100%"
                ),
                rx.cond(
                    ~ProductState.search_query,
                    products_section()
                )
            ),
            
            footer(),
            width="100%",
            spacing="0",
            bg="#f9fafb"
        ),
        # Chatbot overlay
        rx.box(
            chatbot(),
            position="fixed",
            bottom="2rem",
            right="2rem",
            z_index="1000"
        ),
        cart_sidebar(),
        width="100%"
    )