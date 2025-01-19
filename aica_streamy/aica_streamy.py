"""Create a simple chat, which scrolls correctly."""

import asyncio
from typing import Any

import reflex as rx
import reflex.event as ev
import reflex_chakra as rc

# test
#from reflex_intersection_observer import intersection_observer
#from reflex_intersection_observer import IntersectionObserverEntry
from aica_streamy.test import intersection_observer
from aica_streamy.test import IntersectionObserverEntry

# my files
import aica_streamy.content as content

STYLESHEETS = [
    "/css/stylesheet.css",
]

BOTTOM_ELEMENT_ID = "bottom"


class ScrollHandlingState(rx.State):
    @rx.event
    def scroll_to_bottom(self):
        return rx.call_script(
            f"document.getElementById('{BOTTOM_ELEMENT_ID}').scrollIntoView()"
        )
    
    @rx.event
    def handle_non_intersect(self, entry: IntersectionObserverEntry) -> ev.EventSpec:
        print(f"Non-intersected! {entry}")
        return self.scroll_to_bottom()


class MessageGenerator(rx.State):
    parts = list(content.markdown2)
    index = 0
    messages: list[str]
    should_load: bool = False
    button_text: str

    @rx.event
    def stop(self):
        self.on_load()        

    @rx.event
    def on_load(self):
        self.index = 0
        self.messages = []
        self.should_load = False
        self.button_text = "Start"

    @rx.event
    def start(self):
        self.on_load()
        self.should_load = True
        self.button_text = "Restart"
        return MessageGenerator.add_messages

    @rx.event(background=True)
    async def add_messages(self):
        while self.should_load:
            async with self:
                if len(self.messages) == 0:
                    self.messages.append(f"{self.parts[self.index]}")
                    self.index += 1
                else:
                    tmp = self.messages[-1]
                    tmp += f"{self.parts[self.index]}"
                    self.messages[-1] = tmp
                    self.index += 1
                if not self.should_load:
                    self.index = 0
                    break
                if self.index == len(self.parts) - 1:
                    self.index = 0
                    self.should_load = False
                    break
            await asyncio.sleep(0.06)
            yield ScrollHandlingState.scroll_to_bottom


def index() -> rx.Component:
    return rx.vstack(
        rx.tooltip(
            rx.heading("Stream chat emulator"),
            content="emulate the response of an LLM from a long markdown string.",
        ),
        rx.hstack(
            rx.button(
                MessageGenerator.button_text,
                on_click=[
                    MessageGenerator.start,
                    MessageGenerator.add_messages,
                ],
            ),
            rx.button("Stop", on_click=MessageGenerator.stop),
        ),
        rx.center(
            rx.scroll_area(
                rx.vstack(
                    rx.foreach(MessageGenerator.messages, rx.markdown),
                    intersection_observer(
                        height="1px",
                        id=BOTTOM_ELEMENT_ID,
                        root="#scroller",
                        on_non_intersect=ScrollHandlingState.handle_non_intersect,
                        visibility="hidden",
                    ),
                ),
                id="scroller",
                width="50vw",
                height="80vh",
                bg="gray",
                padding="10px",
                border_radius="10px",
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
                            width=["15em", "20em", "45em", "50em", "50em", "50em"],
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
                # on_submit=<STATE>.process_question,
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
    )


app = rx.App(stylesheets=STYLESHEETS)
app.add_page(index, on_load=MessageGenerator.on_load)
