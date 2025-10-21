from threading import Thread
from queue import Queue
from app.chat.callbacks.stream import StreamingHandler
from flask import current_app


class StreamableChain:
    # override the default chain.stream method
    def stream(self, input):
        # separate queue and handler for each streaming chain instance
        queue = Queue()
        handler = StreamingHandler(queue)

        # self(input) # waits for entire response before proceeding to while loop
        # solution: run in separate thread (concurrent)
        def task(app_context):
            app_context.push()
            self(input, callbacks=[handler])

        Thread(target=task, args=[current_app.app_context()]).start()

        while True:
            token = queue.get()  # waits for something to be added to queue
            if token is None:
                break
            yield token
