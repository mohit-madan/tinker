class Context:
    def __init__(self, input_data):
        self.data = input_data # data is the input data
        self.state = {} # state is the memory

class Node:
    def execute(self, ctx):
        raise NotImplementedError()

class ActionNode(Node):
    def __init__(self, func, next_node_id):
        self.func = func
        self.next_node_id = next_node_id
    
    def execute(self, ctx):
        result = self.func(ctx)
        ctx.state.update(result)
        return self.next_node_id

class DecisionNode(Node):
    def __init__(self, logic_func, branches):
        self.logic_func = logic_func
        self.branches = branches # Dict: { result_key : next_node_id }

    def execute(self, ctx):
        result = self.logic_func(ctx)
        next_node_id = self.branches[result]
        return next_node_id

class LLMDecisionNode(Node):
    def __init__(self, prompt_template, branches):
        self.prompt_template = prompt_template
        self.branches = branches
    
    def execute(self, ctx):
        prompt = self.prompt_template.format(**ctx.data, **ctx.state)
        llm_response = call_llm(prompt).strip().upper()


class ResultNode(Node):
    def __init__(self, score):
        self.score = score
    
    def execute(self, ctx):
        return None # Returning None signals "Stop"

#engine
def run_eval_graph(start_node_id, nodes, input_data):
    ctx = Context(input_data)
    current_node_id = start_node_id

    while current_node_id:
        print(f"Executing node {current_node_id}")
        node = nodes[current_node_id]

        if isinstance(node, ResultNode):
            return node.score
        
        current_node_id = node.execute(ctx)

def call_llm(prompt):
    return "True"

def extract_headings_logic(ctx):
    text = ctx.data["text"]

def check_missing_headings_logic(ctx):
    return True

def check_order_headings_logic(ctx):
    return True


nodes_registry = {
    "extract": ActionNode(
        func=extract_headings_logic, 
        next_node_id="check_missing"
    ),
    "check_missing": DecisionNode(
        logic_func=check_missing_headings_logic,
        branches={
            "True": "check_order",
            "False": "score_0"
        }
    ),
    "check_order": DecisionNode(
        logic_func=check_order_headings_logic,
        branches={
            "True": "score_2",
            "False": "score_1"
        }
    ),
    "score_0": ResultNode(score=0),
    "score_1": ResultNode(score=1),
    "score_2": ResultNode(score=2),
}

run_eval_graph("extract", nodes_registry, {"text": "Here is the intro, then the body, finally conclusion"})