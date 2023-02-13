from abc import ABC


# --- Strategy design pattern implementation ---

class BaseState(ABC):
    state_item = []

    def set_context(self, context):
        for i in range(len(context)):
            context[i].set_enabled(self.state_item[i])