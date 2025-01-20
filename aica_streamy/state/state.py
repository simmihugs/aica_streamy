import asyncio
from dataclasses import dataclass
from typing import Any

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

class MessageGenerator(rx.State):
    parts = list(content.markdown2)
    index = 0
    question: list[str]
    messages: list[Message]
    should_load: bool = False
    button_text: str

    @rx.event
    def process_question(self, data: dict[str, Any]):
        self.question = list(data["question"])
        print(self.question)
        return MessageGenerator.start

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
    async def start(self):
        self.on_load()
        self.should_load = True
        self.button_text = "Restart"
        self.messages = []
        self.index = 0
        return MessageGenerator.add_question

    @rx.event(background=True)
    async def add_question(self):
        while self.should_load:
            async with self:                
                if self.messages == []:
                    self.messages.append(Message(sub_type="question", text=""))

                if self.index < len(self.question):
                    self.messages[-1].text += f"{self.question[self.index]}"
                    print(f"{self.index=}") 
                    print(f"'{self.messages[-1].text}'")
                    self.index += 1
                else:
                    print(f"{self.index=}")                    
                    self.index = 0
                    self.question = []
                    break
                
            await asyncio.sleep(0.06)
            yield ScrollHandlingState.scroll_to_bottom
        yield MessageGenerator.add_answer
            
    @rx.event(background=True)
    async def add_answer(self):
        while self.should_load:
            async with self:                
                if self.messages[-1].sub_type == "question":
                    self.messages.append(Message(sub_type="answer", text=""))
                
                if self.index < len(self.parts):
                    self.messages[-1].text += f"{self.parts[self.index]}"
                    self.index += 1
                else:
                    self.index = 0
                    self.should_load = False                    
                    break
            await asyncio.sleep(0.06)
            yield ScrollHandlingState.scroll_to_bottom
            
