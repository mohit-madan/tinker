
class StateContext:
    def __init__(self):
        self.history: List[Dict] = []
        self.data: Dict[str, Any] = {}
        self.current_state: str = "GATHER"
    
    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

class BaseNode:
    def __init__(self):
        # The Global "Constitution" - Always present
        self.global_prompt = (
            "You are a polite Microsoft Support Agent. "
            "Help the user efficiently. Speak in concise English."
        )
    

    @property
    @abstractmethod
    def system_instruction(self) -> str:
        """The specific goal for this state."""
        pass
    