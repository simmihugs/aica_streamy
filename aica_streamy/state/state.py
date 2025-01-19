import asyncio
from dataclasses import dataclass

import reflex as rx
import reflex.event as ev

import aica_streamy.content as content

BOTTOM_ELEMENT_ID = "bottom"


@dataclass
class Message:
    text: str
    sub_type: str

class ScrollHandlingState(rx.State):
    @rx.event
    def scroll_to_bottom(self):
        return rx.call_script(
            f"document.getElementById('{BOTTOM_ELEMENT_ID}').scrollIntoView()"
        )

    #@rx.event
    #def do_nothing(self):
    #    return rx.call_script("console.log('hello, world!')")


class MessageGenerator(rx.State):
    parts = list(content.markdown2)
    index = 0
    messages: list[Message]
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
        self.messages = [Message(sub_type="question", text="Give me some random facts!")]
        return MessageGenerator.add_messages

    @rx.event(background=True)
    async def add_messages(self):
        while self.should_load:
            async with self:
                if self.messages[-1].sub_type == "question":
                    self.messages.append(Message(sub_type="answer", text=f"{self.parts[self.index]}"))
                    self.index += 1
                else:
                    self.messages[-1].text += f"{self.parts[self.index]}"
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
