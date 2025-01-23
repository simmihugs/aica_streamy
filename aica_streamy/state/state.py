import time
import asyncio
from dataclasses import dataclass
from typing import Any

import reflex as rx

import os
from dotenv import dotenv_values, load_dotenv

load_dotenv()
if not os.getenv("GEMINI_API_KEY"):
    raise Exception("Please set GEMINI_API_KEY environment variable.")

keys = {key: value for key, value in dotenv_values().items()}


from google import genai
from google.genai import types

client = genai.Client(api_key=keys["GEMINI_API_KEY"])

BOTTOM_ELEMENT_ID = "bottom"


@dataclass
class Message:
    text: str
    sub_type: str
    id: int
    length: int


class ScrollHandlingState(rx.State):
    @rx.event
    def scroll_to_bottom(self):
        return rx.call_script(
            f"document.getElementById('{BOTTOM_ELEMENT_ID}').scrollIntoView()"
        )

class MessageGenerator(rx.State):
    parts: list[str] = []
    done: bool = False
    index: int = 0
    messages: list[Message]
    should_load: bool = False
    question: str = ""

    @rx.event
    def process_question(self, data: dict[str, Any]):
        self.question = data["question"]
        return MessageGenerator.start

    @rx.event
    def on_load(self):
        self.index = 0
        self.messages = []
        self.should_load = False

    @rx.event
    async def start(self):
        self.should_load = True
        self.index = 0
        return MessageGenerator.add_question

    @rx.event(background=True)
    async def add_question2(self):
        question_characters = list(self.question)
        while self.should_load:
            async with self:
                if self.messages == [] or self.messages[-1].sub_type == "answer":
                    self.messages.append(
                        Message(
                            sub_type="question",
                            text="",
                            id=len(self.messages),
                            length=0,
                        )
                    )

                if self.index < len(question_characters):
                    self.messages[-1].text += f"{question_characters[self.index]}"
                    self.messages[-1].length = self.index
                    self.index += 1
                else:
                    self.index = 0
                    break

            yield ScrollHandlingState.scroll_to_bottom
            await asyncio.sleep(0.03)
        yield MessageGenerator.add_answer
    
    @rx.event
    def add_question(self):
        self.messages.append(Message(sub_type="question",text=self.question, id=len(self.messages), length=0))
        yield ScrollHandlingState.scroll_to_bottom        
        return MessageGenerator.add_answer

    @rx.event(background=True)
    async def add_answer(self):
        async with self:
            self.messages.append(
                Message(sub_type="answer", text="", id=len(self.messages), length=0)
            )

        async for response in client.aio.models.generate_content_stream(
            model="gemini-2.0-flash-exp",
            contents=self.question,
        ):
            for word in str(response.text).split(" "):
                async with self:
                    self.messages[-1].text += f"{word} "
                await asyncio.sleep(0.1)
                yield ScrollHandlingState.scroll_to_bottom()

        async with self:
            self.should_load = False
