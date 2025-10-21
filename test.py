from threading import Thread
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from queue import Queue

load_dotenv()


class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue

    def on_llm_new_token(self, token: str, **kwargs):
        self.queue.put(token)

    def on_llm_end(self, response: LLMResult, **kwargs):
        self.queue.put(
            None
        )  # arbitrary value to signal to StreamingChain.stream that response is done

    def on_llm_error(self, error: BaseException, **kwargs):
        self.queue.put(None)


chat = ChatOpenAI(streaming=True)

prompt = ChatPromptTemplate.from_messages([("human", "{content}")])


class StreamableChain:
    # override the default chain.stream method
    def stream(self, input):
        # separate queue and handler for each streaming chain instance
        queue = Queue()
        handler = StreamingHandler(queue)

        # self(input) # waits for entire response before proceeding to while loop
        # solution: run in separate thread (concurrent)
        def task():
            self(input, callbacks=[handler])

        Thread(target=task).start()

        while True:
            token = queue.get()  # waits for something to be added to queue
            if token is None:
                break
            yield token


# extend any class with StreamableChain to add streaming to chain
class StreamingChain(StreamableChain, LLMChain):
    pass


chain = StreamingChain(llm=chat, prompt=prompt)

for output in chain.stream(input={"content": "tell me a joke"}):
    print(output)


# chain = LLMChain(llm=chat, prompt=prompt)
# # chain.stream doesn't actually steam response
# # custom code required for streaming with chains

# messages = prompt.format_messages(content="tell me a joke")

# # syntax for calling the chat object (eq. to chat.__call__(messages) or .invoke(messages))
# output = chat(messages)
# print(output)
