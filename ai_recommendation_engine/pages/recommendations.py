import reflex as rx
from ..state.recommendation_state import RecommendationState

def recommendations():
    return rx.vstack(
        rx.heading("✨ Recommended for You"),

        rx.input(
            placeholder="Search product...",
            on_change=RecommendationState.set_query
        ),

        rx.button("Get Recommendations", on_click=RecommendationState.generate),

        rx.foreach(
            RecommendationState.results,
            lambda item: rx.box(
                rx.text(item),
                border="1px solid green",
                padding="10px"
            )
        )
    )