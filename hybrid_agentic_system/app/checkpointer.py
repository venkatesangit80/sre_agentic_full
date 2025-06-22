from langgraph.checkpoint.memory import MemorySaver

# For demo: use in-memory saver; in production, use Redis/File/DB
_checkpointer = MemorySaver()

def get_checkpointer():
    return _checkpointer