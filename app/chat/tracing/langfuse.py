import os
from langfuse.client import Langfuse

langfuse = Langfuse(
    os.environ["LANGFUSE_PUBLIC_KEY"],
    os.environ["LANGFUSE_SECRET_KEY"],
    host=os.environ["LANGFUSE_HOST"],
)
# from langfuse import get_client

# langfuse = get_client()
