"""Create a simple chat, which scrolls correctly."""


import reflex as rx

import reflex_chakra as rc

from aica_streamy.state import MessageGenerator, BOTTOM_ELEMENT_ID, Message


STYLESHEETS = [
    "/css/stylesheet.css",
]


def copy_button(message: Message) -> rx.Component:
    return (
        rx.box(
            rx.cond(
                (~MessageGenerator.should_load) | MessageGenerator.messages[-1].id
                != message.id,
                rx.hstack(
                    rx.el.button(
                        rx.icon(tag="copy", size=18),
                    ),
                    rx.text(
                        "copy",
                    ),
                    _hover={"color": rx.color("accent", 8)},
                    on_click=[
                        rx.set_clipboard(message.text),
                        rx.toast("Copied answer to clipboard"),
                    ],
                ),
            ),
            margin_left="5px",
            margin_bottom="2px",
        ),
    )


def create_bubble(message: Message) -> rx.Component:
    config = dict(
        width="40vw", padding="10px", border_radius="20px", display="inline-block"
    )
    return rx.cond(
        message.sub_type == "answer",
        rx.box(
            rx.markdown(
                message.text,
                margin="20px",
            ),
            copy_button(message),
            bg=rx.color("accent", 4),
            margin_right="auto",
            **config,
        ),
        rx.box(
            rx.markdown(
                message.text,
            ),
            bg=rx.color("accent", 6),
            margin_left="auto",
            **config,
        ),
    )


def input() -> rx.Component:
    return (
        rx.center(
            rc.form(
                rc.form_control(
                    rx.hstack(
                        rx.input(
                            rx.input.slot(
                                rx.tooltip(
                                    rx.icon("info", size=18),
                                    content="Enter a question to get a response.",
                                )
                            ),
                            placeholder="Type something...",
                            id="question",
                            width=[
                                "15em",
                                "20em",
                                "45em",
                                "50em",
                                "50em",
                                "50em",
                            ],
                        ),
                        rx.button(
                            "Send",
                            loading=MessageGenerator.should_load,
                            type="submit",
                            background_color=rx.color("accent", 4),
                            color=rx.color("accent", 12),
                        ),
                        align_items="center",
                    ),
                    is_disabled=MessageGenerator.should_load,
                    padding_left="10px",
                    padding_right="10px",
                ),
                on_submit=MessageGenerator.process_question,
                reset_on_submit=True,
                position="sticky",
                bottom="0",
                padding_y="16px",
                backdrop_filter="auto",
                backdrop_blur="lg",
                border_top=f"1px solid {rx.color('mauve', 3)}",
                background_color=rx.color("mauve", 2),
                align_items="stretch",
            ),
        ),
    )


def scroll():
    return rx.center(
        rx.scroll_area(
            rx.vstack(
                rx.foreach(MessageGenerator.messages, create_bubble),
                rx.text(
                    "",
                    id=BOTTOM_ELEMENT_ID,
                    visibility="hidden",
                    margin_top="20xp",
                ),
            ),
            flex="1",
            id="scroller",
            width="50vw",
            height="80vh",
            padding="10px",
            margin="10px",
            type="auto",
        ),
    )


def selection_box() -> rx.Component:
    return (
        rx.vstack(
            rx.box(
                rx.vstack(
                    rx.heading("LLM API"),
                    rx.radio(
                        ["anthropic", "gemini", "openai", "mistral"],
                        on_change=MessageGenerator.set_api,
                        direction="row",
                        default_value="anthropic",
                    ),
                ),
                padding="20px",
                border_radius="10px",
                bg=rx.color("gray", 5),
            ),
            width="50%",
            height="100%",
            padding="20px",
        ),
    )


def index() -> rx.Component:
    return rx.hstack(
        selection_box(),
        rx.vstack(
            rx.heading("LLM Chat"),
            scroll(),
            input(),
            align="center",
            min_height="100vh",
            padding_top="20px",
        ),
    )


app = rx.App(stylesheets=STYLESHEETS, theme=rx.theme(accent_color="grass"))
app.add_page(index, on_load=MessageGenerator.on_load)
