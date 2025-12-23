import chainlit as cl

from startup_sim.ui_logic import handle_message


@cl.on_chat_start
async def start_chat():
    await cl.Message(content="Team ready. Describe your objective to begin.").send()


@cl.on_message
async def on_message(message: cl.Message):
    await cl.Message(content="Planning team response...").send()
    final_text = await handle_message(message.content)
    await cl.Message(content=final_text).send()
