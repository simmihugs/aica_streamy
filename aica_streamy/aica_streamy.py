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
                        on_click=[
                            rx.set_clipboard(message.text),
                            rx.toast("Copied!"),
                        ],
                        _hover={"color": rx.color("accent", 8)},
                    ),
                    rx.text("copy"),
                ),
            ),
            margin="10px",
        ),
    )


def p(message: Message) -> rx.Component:
    return rx.cond(
        #rx.box(
            #rx.cond(
                True,
                rx.text("", hidden=True,),
            ),
            #hidden=True,
        #),
    #)
def p2(message: Message) -> rx.Component:
    return rx.text(message)


def create_bubble(message: Message) -> rx.Component:
    return rx.cond(
        message.sub_type == "answer",
        rx.box(
            rx.cond(
                message.length > 400,
                copy_button(message),
                p(message),
            ),
            rx.markdown(
                message.text,
                margin="20px",
            ),
            copy_button(message),
            width="40vw",
            border_radius="10px",
            bg=rx.color("accent", 4),
            display="inline-block",
            text_align="left",
            margin_right="auto",
        ),
        rx.box(
            rx.markdown(
                message.text,
            ),
            width="40vw",
            padding="20px",
            border_radius="10px",
            bg=rx.color("accent", 6),
            display="inline-block",
            text_align="left",
            margin_left="auto",
        ),
    )


def generate_list(message: Message) -> rx.Component:
    m: str = message.text[:15]
    return rx.cond(
        message.sub_type == "question",
        rx.box(rx.text(f"question: {m}"), bg=rx.color("accent", 4)),
        rx.box(rx.text(f"answer: {m}"), bg=rx.color("accent", 6)),
    )


def index() -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.vstack(
                rx.heading("Hello"),
                rx.foreach(MessageGenerator.messages, generate_list),
            ),
            padding="20px",
            border_radius="10px",
            margin="20px",
            bg=rx.color("gray", 5),
            width="50%",
            height="100%",
        ),
        rx.vstack(
            rx.tooltip(
                rx.heading("Stream chat emulator"),
                content="emulate the response of an LLM from a long markdown string.",
            ),
            rx.center(
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
            ),
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
            align="center",
            min_height="100vh",
        ),
    )


app = rx.App(stylesheets=STYLESHEETS, theme=rx.theme(accent_color="grass"))
app.add_page(index, on_load=MessageGenerator.on_load)
