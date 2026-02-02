# Core entities
# AgentState: represents the state of an agent
# AssignmentSystem: manages the assignment of conversations to agents
# 
# Core operations
# set_limit: set the limit of an agent
# assign: assign a conversation to an agent
# preview_assignment: preview the assignment of conversations to agents
# release: release an agent from a conversation

class AgentState:
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.limit = 2
        self.load = 0
        self.last_assigned_seq = 0
    
    def copy(self):
        # helper to create copy for a simulation
        new_agent = AgentState(self.name, self.index)
        new_agent.limit = self.limit
        new_agent.load = self.load
        new_agent.last_assigned_seq = self.last_assigned_seq
        return new_agent
    

class AssignmentSystem:
    def __init__(self, agents):
        self.agents = [AgentState(agent, i) for i, agent in enumerate(agents)]
        self.seq_counter = 1

    def set_limit(self, agent_name, limit):
        for agent in self.agents:
            if agent.name == agent_name:
                agent.limit = limit
                return
        raise ValueError(f"Agent {agent_name} not found")

    def select_next(self, agent_pool):
        available_agents = [a for a in agent_pool if a.load < a.limit]
        if not available_agents:
            return None
        
        available_agents.sort(
            key = lambda x: (x.load, x.last_assigned_seq, x.index)
        )
        return available_agents[0]
    
    def assign(self, conversation_id):
        agent = self.select_next(self.agents)
        if not agent:
            return None
        agent.load += 1
        agent.last_assigned_seq = self.seq_counter
        self.seq_counter += 1
        return agent.name
    
    def preview_assignment(self, n):
        # 1. Clone the agents using the helper method
        sim_agents = [a.clone() for a in self.agents]        
        sim_seq = self.seq_counter
        result = []

        # 2. Run simulation
        for _ in range(n):
            agent = self.select_next(sim_agents)
            if not agent:
                result.append(None)
                continue
            result.append(agent.name)
            agent.load += 1
            agent.last_assigned_seq = sim_seq
            sim_seq += 1
        return result

    def release(self, agent_name):
        for agent in self.agents:
            if agent.name == agent_name:
                if agent.load > 0:
                    agent.load -= 1
                    return True
                else:
                    raise ValueError(f"Agent {agent_name} is not assigned any conversations")
        raise ValueError(f"Agent {agent_name} not found")