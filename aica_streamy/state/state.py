import time
import asyncio
from dataclasses import dataclass
from typing import Any

import reflex as rx

# import reflex.event as ev

# import aica_streamy.content as content

import os
from dotenv import dotenv_values, load_dotenv

load_dotenv()
if not os.getenv("GEMINI_API_KEY"):
    raise Exception("Please set GEMINI_API_KEY environment variable.")

keys = {key: value for key, value in dotenv_values().items()}
# import google.generativeai as genai

from google import genai
from google.genai import types

# Only run this block for Gemini Developer API
client = genai.Client(api_key=keys["GEMINI_API_KEY"])
# genai.configure(api_key=keys["GEMINI_API_KEY"])
# model = genai.GenerativeModel("gemini-2.0-flash-exp")
# chat = model.start_chat(history=[])


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


async def fill_bucket(model, prompt, queue):
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        print("fill bucket")
        if (answer := chunk.text) is not None:
            await queue.put(answer)
    await queue.put(None)


async def empty_bucket(mg, queue):
    while mg.should_load:
        print("empty bucket")
        chunk = await queue.get()
        if chunk is None:
            break

        # yield sg.scroll_to_bottom
        # yield ScrollHandlingState.scroll_to_bottom
        async with mg:
            if mg.messages[-1].sub_type == "question":
                print(f"{time.time()}: added question")
                mg.messages.append(
                    Message(sub_type="answer", text="", id=len(mg.messages), length=0)
                )
            mg.messages[-1].text += chunk

        # yield ScrollHandlingState.scroll_to_bottom
        await asyncio.sleep(0.3)
    # yield ScrollHandlingState.scroll_to_bottom


class MessageGenerator(rx.State):
    parts: list[str] = []
    done: bool = False
    index: int = 0
    question: list[str]
    messages: list[Message]
    should_load: bool = False
    q: str = ""

    @rx.event
    def process_question(self, data: dict[str, Any]):
        self.q = data["question"]
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
                    self.messages.append(
                        Message(
                            sub_type="question",
                            text="",
                            id=len(self.messages),
                            length=0,
                        )
                    )

                if self.index < len(self.question):
                    self.messages[-1].text += f"{self.question[self.index]}"
                    self.messages[-1].length = self.index
                    self.index += 1
                else:
                    self.index = 0
                    self.question = []
                    break

            yield ScrollHandlingState.scroll_to_bottom
            await asyncio.sleep(0.03)
        yield MessageGenerator.add_answer
        # yield MessageGenerator.StartProcess

    # @rx.event(background=True)
    # async def add_answer_old(self):
    #     response = chat.send_message(
    #         self.messages[-1].text,
    #         stream=True,
    #     )
    #     async with self:
    #         self.parts = []
    #         self.index = 0
    #         for chunk in response:
    #             if (answer := chunk.text) is not None:
    #                 self.parts.append(answer)

    #     while self.should_load:
    #         yield ScrollHandlingState.scroll_to_bottom
    #         await asyncio.sleep(0.3)
    #         async with self:
    #             if self.messages[-1].sub_type == "question":
    #                 print(f"{time.time()}: added question")
    #                 self.messages.append(
    #                     Message(
    #                         sub_type="answer", text="", id=len(self.messages), length=0
    #                     )
    #                 )

    #             if self.index < len(self.parts):
    #                 self.messages[-1].text += f"{self.parts[self.index]}"
    #                 self.messages[-1].length = self.index
    #                 self.index += 1
    #             else:
    #                 self.index = 0
    #                 self.should_load = False
    #                 break

    #         yield ScrollHandlingState.scroll_to_bottom
    #         await asyncio.sleep(0.3)
    #     yield ScrollHandlingState.scroll_to_bottom

    # @rx.event(background=True)
    # async def StartProcess(self):
    #     queue = asyncio.Queue()
    #     generate_task = asyncio.create_task(
    #         fill_bucket(model=model, prompt=self.messages[-1].text, queue=queue)
    #     )
    #     update_ui_task = asyncio.create_task(empty_bucket(mg=self, queue=queue))
    #     await asyncio.gather(generate_task, update_ui_task)

    # @rx.event(background=True)
    # async def add_answer3(self):
    #     queue = asyncio.Queue()

    #     async def producer():
    #         response = chat.send_message(self.messages[-1].text, stream=True)
    #         for chunk in response:
    #             if (answer := chunk.text) is not None:
    #                 await queue.put(answer)
    #         await queue.put(None)  # Signal end of stream

    #     async def consumer():
    #         async with self:
    #             self.messages.append(
    #                 Message(sub_type="answer", text="", id=len(self.messages), length=0)
    #             )

    #         while True:
    #             chunk = await queue.get()
    #             if chunk is None:
    #                 break

    #             async with self:
    #                 self.messages[-1].text += chunk
    #                 self.messages[-1].length += len(chunk)

    #             rx.call_script(
    #                 f"document.getElementById('{BOTTOM_ELEMENT_ID}').scrollIntoView()"
    #             )

    #             await asyncio.sleep(0.1)

    #         # self.should_load = False
    #         rx.call_script(
    #             f"document.getElementById('{BOTTOM_ELEMENT_ID}').scrollIntoView()"
    #         )

    #     # Run producer and consumer concurrently
    #     await asyncio.gather(producer(), consumer())

    @rx.event(background=True)
    async def add_answer(self):
        async with self:
            self.messages.append(
                Message(sub_type="answer", text="", id=len(self.messages), length=0)
            )

        async for response in client.aio.models.generate_content_stream(
            model="gemini-2.0-flash-exp",
            contents=self.q,
        ):
            for word in str(response.text).split(" "):
                async with self:
                    self.messages[-1].text += f"{word} "
                await asyncio.sleep(0.1)
                yield ScrollHandlingState.scroll_to_bottom()

        async with self:
            self.should_load = False
