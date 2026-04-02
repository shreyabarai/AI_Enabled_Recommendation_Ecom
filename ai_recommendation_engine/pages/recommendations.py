import reflex as rx
from ..state.recommendation_state import RecommendationState
from ..components.product_card import product_card
from ..components.navbar import navbar
from ..components.footer import footer

def recommendations():
    return rx.box(
        navbar(),
        rx.vstack(
            # Search / Trigger Section
            rx.vstack(
                rx.heading("AI Recommendation Center", size="8", weight="bold", color="#111827"),
                rx.text("Get personalized product suggestions powered by machine learning", color="#374151"),
                rx.hstack(
                    rx.input(
                        placeholder="Search for products to get recommendations...",
                        on_change=RecommendationState.set_query,
                        width="400px",
                        radius="full",
                        bg="white"
                    ),
                    rx.button(
                        "Generate Recommendations",
                        on_click=RecommendationState.generate_recommendations,
                        bg="#10b981",
                        color="white",
                        radius="full",
                        loading=RecommendationState.is_loading
                    ),
                    spacing="4",
                    margin_top="1.5rem"
                ),
                padding="4rem",
                bg="#f0fdf4",
                width="100%",
                align_items="center"
            ),

            rx.cond(
                RecommendationState.is_loading,
                rx.center(
                    rx.vstack(
                        rx.spinner(size="3", color="#10b981"),
                        rx.text("Our AI is crunching data for you...", weight="medium"),
                        spacing="4",
                        padding="4rem"
                    ),
                    width="100%"
                ),
                rx.vstack(
                    # Section 1: Content-based
                    rx.cond(
                        RecommendationState.content_results.length() > 0,
                        rx.vstack(
                            rx.vstack(
                                rx.heading("Because you viewed", size="7", weight="bold", color="#111827"),
                                rx.text("Products similar to your recent interests", color="#6b7280"),
                                align_items="start",
                                spacing="1",
                                margin_bottom="2rem"
                            ),
                            rx.grid(
                                rx.foreach(RecommendationState.content_results, product_card),
                                columns="4",
                                spacing="6",
                                width="100%"
                            ),
                            padding="4rem",
                            width="100%",
                            align_items="start"
                        )
                    ),

                    # Section 2: Collaborative-based
                    rx.cond(
                        RecommendationState.collaborative_results.length() > 0,
                        rx.vstack(
                            rx.vstack(
                                rx.heading("Users like you also liked", size="7", weight="bold", color="#111827"),
                                rx.text("Trending items based on community preferences", color="#6b7280"),
                                align_items="start",
                                spacing="1",
                                margin_bottom="2rem"
                            ),
                            rx.grid(
                                rx.foreach(RecommendationState.collaborative_results, product_card),
                                columns="4",
                                spacing="6",
                                width="100%"
                            ),
                            padding="4rem",
                            width="100%",
                            align_items="start"
                        )
                    ),

                    # Empty State
                    rx.cond(
                        (RecommendationState.content_results.length() == 0) & 
                        (RecommendationState.collaborative_results.length() == 0) & 
                        (~RecommendationState.is_loading),
                        rx.center(
                            rx.vstack(
                                rx.icon(tag="sparkles", size=60, color="#d1d5db"),
                                rx.text("Start searching to see personalized recommendations!", color="#6b7280"),
                                spacing="4",
                                padding="6rem"
                            ),
                            width="100%"
                        )
                    ),
                    width="100%"
                )
            ),
            footer(),
            width="100%",
            spacing="0",
            bg="#f9fafb"
        )
    )