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


# gemini
from google import genai
from google.genai import types

client_gemini = genai.Client(api_key=keys["GEMINI_API_KEY"])

# openai
#import openai
from openai import AsyncOpenAI

client_openai = AsyncOpenAI(api_key=keys["OPENAI_API_KEY"])

# anthropic
from anthropic import AsyncAnthropic

client_anthropic = AsyncAnthropic(api_key=keys["ANTHROPIC_API_KEY"])

# mistral
from mistralai import Mistral, UserMessage
#from mistralai.async_client import MistralAsyncClient
#from mistralai.models.chat_completion import ChatMessage
#client_mistral = MistralAsyncClient(api_key=keys["MISTRAL_API_KEY"])
client_mistral = Mistral(api_key=keys["MISTRAL_API_KEY"])


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
    api: str = "anthropic"

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
        self.messages.append(
            Message(
                sub_type="question", text=self.question, id=len(self.messages), length=0
            )
        )
        yield ScrollHandlingState.scroll_to_bottom
        
        match self.api:
            case "google":
                return MessageGenerator.add_answer_google
            case "openai":
                return MessageGenerator.add_answer_openai
            case "anthropic":
                return MessageGenerator.add_answer_anthropic
            case "mistral":
                return MessageGenerator.add_answer_mistral
            case _:
                return MessageGenerator.add_answer_gemini

    @rx.event(background=True)
    async def add_answer_google(self):
        async with self:
            self.messages.append(
                Message(sub_type="answer", text="", id=len(self.messages), length=0)
            )

        async for response in client_gemini.aio.models.generate_content_stream(
            model="gemini-2.0-flash-exp",
            contents=self.question,
        ):
            for character in list(response.text):
                async with self:
                    self.messages[-1].text += f"{character}"
                await asyncio.sleep(0.1)
                yield ScrollHandlingState.scroll_to_bottom()

        async with self:
            self.should_load = False

    @rx.event(background=True)
    async def add_answer_openai(self):
        async with self:
            self.messages.append(
                Message(sub_type="answer", text="", id=len(self.messages), length=0)
            )

        stream = await client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": self.question}],
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                for character in list(chunk.choices[0].delta.content):
                    async with self:
                        self.messages[-1].text += f"{character}"
                    await asyncio.sleep(0.025)
                    yield ScrollHandlingState.scroll_to_bottom()

        async with self:
            self.should_load = False


    @rx.event(background=True)
    async def add_answer_anthropic(self):
        async with self:
            self.messages.append(
                Message(sub_type="answer", text="", id=len(self.messages), length=0)
            )

        stream = await client_anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": self.question}],
            max_tokens=1024,
            stream=True
        )

        async for chunk in stream:
            if chunk.type == "content_block_delta" and chunk.delta.type == "text_delta":
                characters = list(chunk.delta.text)
                for character in characters:
                    async with self:
                        self.messages[-1].text += f"{character}"
                    await asyncio.sleep(0.025)
                    yield ScrollHandlingState.scroll_to_bottom()

        async with self:
            self.should_load = False


    @rx.event(background=True)
    async def add_answer_mistral(self):
        async with self:
            self.messages.append(
                Message(sub_type="answer", text="", id=len(self.messages), length=0)
            )   
    
        stream = await client_mistral.chat.stream_async(
            model="mistral-large-latest",
            messages=[UserMessage(content=self.question)]
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                characters = list(chunk.choices[0].delta.content)
                for character in characters:
                    async with self:
                        self.messages[-1].text += f"{character}"
                    await asyncio.sleep(0.025)
                    yield ScrollHandlingState.scroll_to_bottom()

        async with self:
            self.should_load = False
