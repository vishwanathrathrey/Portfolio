"""All prompts live here so they can be unit-tested without hitting the LLM."""


def planner_system_prompt() -> str:
    """Return the strict JSON system prompt for document planning."""
    return (
        "You are a planning engine. You will receive a business request. Output STRICT "
        "JSON only — no prose, no markdown fences. JSON schema: "
        "{{doc_type, title, assumptions[], todos[{{id, description, tool, tool_args, "
        "depends_on}}]}}. Allowed doc_type values: proposal, meeting_minutes, "
        "project_plan, business_report, technical_design, sop, product_spec. Allowed "
        "tool values are ONLY: generate_outline, generate_section_content, "
        "mock_data_provider, render_docx. Do NOT use add_table. Rules: (a) 4-10 todos; "
        "(b) final todo "
        "MUST be render_docx; (c) first todo MUST be generate_outline; (d) if the "
        "request is ambiguous, list each assumption explicitly in assumptions; "
        "(e) no cyclic depends_on; (f) for the render_docx tool, do NOT provide any "
        "tool_args. The executor will automatically inject the document and output_path; "
        "(g) if using generate_section_content, you MUST provide tool_args: "
        '{"section_type": "the_section_name"}.'
    )


def planner_user_prompt(user_request: str, session_context: str | None) -> str:
    """Return the planning prompt for a particular user request."""
    context = ""
    if session_context is not None:
        context = f"Prior session context: {session_context}\n\n"
    return f"{context}Business request:\n{user_request}"


def section_writer_system_prompt() -> str:
    """Return the system prompt for writing one document section."""
    return (
        "You write ONE section of a business document. Plain prose. 120-220 words. "
        "No markdown, no headings, no bullet markers. Use concrete details from the "
        "provided data. Do not invent facts not present in the data."
    )


def section_writer_user_prompt(
    doc_type: str,
    doc_title: str,
    section_title: str,
    data_block: str,
) -> str:
    """Return a structured, data-grounded section-writing prompt."""
    return (
        f"Document type: {doc_type}\n"
        f"Document title: {doc_title}\n"
        f"Section title: {section_title}\n\n"
        "The following data block is the ONLY source of truth. Do not add facts that "
        "are not present in it.\n"
        f"DATA BLOCK:\n{data_block}"
    )


def reflector_system_prompt() -> str:
    """Return the strict JSON system prompt for reviewing plan execution."""
    return (
        "You review a completed plan against the original request. Output STRICT JSON: "
        "{{covered: bool, gaps: [], followup_todos: [{{description, tool, tool_args}}]}}. "
        "followup_todos MUST be empty if covered=true."
    )


def reflector_user_prompt(
    original_request: str,
    plan_json: str,
    results_json: str,
) -> str:
    """Return the reflection prompt with original request, plan, and results."""
    return (
        f"Original request:\n{original_request}\n\n"
        f"Plan JSON:\n{plan_json}\n\n"
        f"Execution results JSON:\n{results_json}"
    )


def mock_data_system_prompt() -> str:
    """Return the strict JSON system prompt for plausible mock business data."""
    return (
        "Return STRICT JSON: {{entities: {{name: {{...}}}}}}. Realistic plausible "
        "business data. No prose."
    )


def mock_data_user_prompt(entity: str, context: str) -> str:
    """Return the mock-data prompt for an entity and its business context."""
    return f"Entity: {entity}\nContext: {context}"
