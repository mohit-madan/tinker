## cursor pseudo code
plan = llm.create_plan(user_input, repo_context)

state = {}

for step in plan:
    tool_call = llm.choose_tool(step, state)
    output = run(tool_call)
    state.update(output)

    if output.has_error:
        plan = llm.replan(state)