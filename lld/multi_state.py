import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

# ==========================================
# 1. State Context (The "Memory")
# ==========================================
class StateContext:
    def __init__(self):
        self.history: List[Dict] = []       # Chat history
        self.data: Dict[str, Any] = {}      # Extracted entities (Order ID, etc.)
        self.current_state: str = "GATHER"  # Start state

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

# ==========================================
# 2. Abstract Node (The "Logic")
# ==========================================
class BaseNode(ABC):
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

    @abstractmethod
    def tools(self) -> List[Dict]:
        """Tools available in this state."""
        pass

    def build_prompt(self, context: StateContext) -> List[Dict]:
        """
        Constructs the Dynamic Prompt Stack.
        Pattern: [Global + State Instructions] + [History]
        """
        # We explicitly tell the LLM about the state change to fix Context Dissonance
        full_system_msg = (
            f"{self.global_prompt}\n"
            f"--------------------------------------------------\n"
            f"CURRENT PHASE: {context.current_state}\n"
            f"INSTRUCTIONS: {self.system_instruction}\n"
            f"NOTE: Previous messages may belong to past phases. Focus on CURRENT instructions."
        )
        
        return [{"role": "system", "content": full_system_msg}] + context.history

    async def execute(self, context: StateContext, llm_response: Dict) -> str:
        """
        Processes LLM output. Returns the NEXT state name.
        """
        # default: stay in same state if no tool called
        return context.current_state

# ==========================================
# 3. Concrete States (The Implementation)
# ==========================================

class GatherInfoNode(BaseNode):
    @property
    def system_instruction(self):
        return "Ask the user for their Order ID. Once obtained, call 'submit_order'."

    def tools(self):
        return [{
            "name": "submit_order",
            "description": "Transition to validation once Order ID is known.",
            "parameters": {"order_id": "string"}
        }]

    async def execute(self, context: StateContext, llm_response: Dict) -> str:
        # Check if LLM wants to call a tool
        tool_call = llm_response.get("tool_call")
        
        if tool_call and tool_call["name"] == "submit_order":
            # 1. Extract Data
            order_id = tool_call["args"]["order_id"]
            context.data["order_id"] = order_id
            print(f"   [System] Order ID captured: {order_id}")
            
            # 2. Transition
            return "VALIDATE"
        
        # Otherwise, just chat
        context.add_message("assistant", llm_response["content"])
        return "GATHER"

class ValidateNode(BaseNode):
    @property
    def system_instruction(self):
        return f"Validate Order ID {self.context_ref.data.get('order_id')}. If valid, say approved."
    
    # We inject context access for dynamic prompts
    def __init__(self, context_ref):
        super().__init__()
        self.context_ref = context_ref

    def tools(self):
        return [] # Terminal state for this demo

    async def execute(self, context: StateContext, llm_response: Dict) -> str:
        context.add_message("assistant", llm_response["content"])
        return "FINISH" # End conversation

# ==========================================
# 4. The Graph Executor (The "Engine")
# ==========================================
class AgentExecutor:
    def __init__(self):
        self.context = StateContext()
        # Registry of nodes
        self.nodes = {
            "GATHER": GatherInfoNode(),
            "VALIDATE": ValidateNode(self.context)
        }

    # MOCK LLM CALL (In interview, just stub this out)
    async def mock_llm_call(self, messages, tools):
        last_user_msg = messages[-1]["content"]
        
        # Simulating LLM Logic
        if "123" in last_user_msg: 
            return {
                "content": None, 
                "tool_call": {"name": "submit_order", "args": {"order_id": "123"}}
            }
        else:
            return {"content": "Could you please provide your Order ID?", "tool_call": None}

    async def run_turn(self, user_input: str):
        # 1. Add User Input
        self.context.add_message("user", user_input)
        
        # 2. Resolve Current Node
        current_node = self.nodes[self.context.current_state]
        
        # 3. Build Prompt (Dynamic System Message)
        messages = current_node.build_prompt(self.context)
        
        # 4. Call LLM
        response = await self.mock_llm_call(messages, current_node.tools())
        
        # 5. Execute Node Logic (State Transition)
        next_state = await current_node.execute(self.context, response)
        
        # 6. Update State
        if next_state != self.context.current_state:
            print(f"   [Transition] {self.context.current_state} -> {next_state}")
            self.context.current_state = next_state
            
            # OPTIONAL: If transition happens, you might want to auto-run the next state immediately
            if next_state == "VALIDATE":
                 # In a real app, we might trigger the next node immediately
                 pass

# ==========================================
# 5. Driver Code (Usage)
# ==========================================
import asyncio

async def main():
    agent = AgentExecutor()
    
    print("--- Turn 1 ---")
    await agent.run_turn("Hi, I need a refund.") 
    # Output: Assistant asks for ID (Stays in GATHER)
    
    print("\n--- Turn 2 ---")
    await agent.run_turn("Sure, my ID is 123.") 
    # Output: LLM detects ID -> Tool Call -> Transitions to VALIDATE

if __name__ == "__main__":
    asyncio.run(main())