import asyncio
from dataclasses import dataclass
from typing import Any

import reflex as rx
import reflex.event as ev

import aica_streamy.content as content

import os
from dotenv import dotenv_values, load_dotenv

load_dotenv()
if not os.getenv("GEMINI_API_KEY"):
    raise Exception("Please set GEMINI_API_KEY environment variable.")

keys = {key: value for key, value in dotenv_values().items()}
import google.generativeai as genai

genai.configure(api_key=keys["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash-exp")
chat = model.start_chat(history=[])

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
    parts: list[str] = []
    done: bool = False
    index: int = 0
    question: list[str]
    messages: list[Message]
    should_load: bool = False

    @rx.event
    def process_question(self, data: dict[str, Any]):
        self.question = list(data["question"])
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
    async def add_question(self):
        while self.should_load:
            async with self:
                if self.messages == [] or self.messages[-1].sub_type == "answer":
                    self.messages.append(Message(sub_type="question", text=""))

                if self.index < len(self.question):
                    self.messages[-1].text += f"{self.question[self.index]}"
                    self.index += 1
                else:
                    self.index = 0
                    self.question = []
                    break

            yield ScrollHandlingState.scroll_to_bottom
            await asyncio.sleep(0.03)
        yield MessageGenerator.add_answer

    @rx.event(background=True)
    async def add_answer(self):
        response = chat.send_message(
            self.messages[-1].text,
            stream=True,
        )
        async with self:
            self.parts = []
            for chunk in response:
                if (answer := chunk.text) is not None:
                    for p in list(answer):
                        self.parts.append(p)
            self.done = True
        await asyncio.sleep(0.03)
        while self.should_load:
            yield ScrollHandlingState.scroll_to_bottom
            async with self:
                if self.messages[-1].sub_type == "question":
                    self.messages.append(Message(sub_type="answer", text=""))

                if self.index < len(self.parts):
                    self.messages[-1].text += f"{self.parts[self.index]}"
                    self.index += 1
                elif self.done:
                    self.index = 0
                    self.should_load = False
                    break
                else:
                    print("waiting for the api response")

            yield ScrollHandlingState.scroll_to_bottom
            await asyncio.sleep(0.015)
