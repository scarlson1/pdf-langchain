from typing import Any, Dict, List
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult


class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue
        self.streaming_run_ids = set()

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        run_id: str,
        **kwargs: Any,
    ):
        print(serialized, run_id)
        if serialized["kwargs"]["streaming"]:
            self.streaming_run_ids.add(run_id)

    def on_llm_new_token(self, token: str, **kwargs):
        self.queue.put(token)

    def on_llm_end(self, response: LLMResult, run_id: str, **kwargs):
        if run_id in self.streaming_run_ids:
            self.queue.put(
                None
            )  # arbitrary value to signal to StreamingChain.stream that response is done
            self.streaming_run_ids.remove(run_id)

    def on_llm_error(self, error: BaseException, **kwargs):
        self.queue.put(None)
