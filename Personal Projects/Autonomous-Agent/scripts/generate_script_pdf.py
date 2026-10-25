"""Generate the structured video-submission script PDF."""

from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)

OUTPUT_PATH = Path("Video_Submission_Script.pdf")
PAGE_WIDTH, PAGE_HEIGHT = A4


class Callout(Flowable):
    """Render a highlighted label and body for recording cues."""

    def __init__(self, label: str, body: str, fill: colors.Color) -> None:
        super().__init__()
        self.label = label
        self.body = body
        self.fill = fill
        self.width = 0.0
        self.height = 0.0

    def wrap(self, available_width: float, available_height: float) -> tuple[float, float]:
        self.width = available_width
        self.height = 38
        return available_width, self.height

    def draw(self) -> None:
        """Draw the callout with a colored label bar."""
        self.canv.setFillColor(self.fill)
        self.canv.roundRect(0, 0, self.width, self.height, 5, fill=1, stroke=0)
        self.canv.setFillColor(colors.white)
        self.canv.setFont("Helvetica-Bold", 9)
        self.canv.drawString(10, 24, self.label.upper())
        self.canv.setFont("Helvetica", 9)
        text = self.body
        max_chars = max(20, int((self.width - 20) / 5.2))
        lines = [text[index : index + max_chars] for index in range(0, len(text), max_chars)]
        for index, line in enumerate(lines[:2]):
            self.canv.drawString(10, 11 - index * 10, line)


def _page_number(canvas: Any, document: BaseDocTemplate) -> None:
    """Draw the footer and page number on every content page."""
    if document.page == 1:
        return
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#CBD5E1"))
    canvas.line(0.7 * inch, 0.55 * inch, PAGE_WIDTH - 0.7 * inch, 0.55 * inch)
    canvas.setFillColor(colors.HexColor("#475569"))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(0.7 * inch, 0.35 * inch, "Autonomous Agent - Video Submission Script")
    canvas.drawRightString(PAGE_WIDTH - 0.7 * inch, 0.35 * inch, f"Page {document.page}")
    canvas.restoreState()


def _styles() -> dict[str, ParagraphStyle]:
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=34,
            textColor=colors.HexColor("#0F172A"),
            spaceAfter=16,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontSize=15,
            leading=21,
            textColor=colors.HexColor("#334155"),
        ),
        "note": ParagraphStyle(
            "Note",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontSize=11,
            leading=16,
            textColor=colors.HexColor("#64748B"),
        ),
        "heading": ParagraphStyle(
            "Heading",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=22,
            textColor=colors.HexColor("#1D4ED8"),
            spaceBefore=12,
            spaceAfter=10,
        ),
        "subheading": ParagraphStyle(
            "Subheading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#0F172A"),
            spaceBefore=8,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            textColor=colors.HexColor("#1E293B"),
            spaceAfter=8,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=styles["Code"],
            fontName="Courier",
            fontSize=8.5,
            leading=12,
            leftIndent=12,
            rightIndent=12,
            backColor=colors.HexColor("#E2E8F0"),
            borderColor=colors.HexColor("#CBD5E1"),
            borderWidth=0.5,
            borderPadding=8,
            textColor=colors.HexColor("#0F172A"),
            spaceBefore=5,
            spaceAfter=10,
        ),
    }


def _paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text.replace("&", "&amp;"), style)


def _section(
    story: list[Flowable],
    styles: dict[str, ParagraphStyle],
    heading: str,
    criterion: str,
) -> None:
    story.append(_paragraph(heading, styles["heading"]))
    story.append(_paragraph(f"<b>Target Criteria:</b> {criterion}", styles["body"]))


def _cue(
    story: list[Flowable],
    styles: dict[str, ParagraphStyle],
    label: str,
    body: str,
    narration: str | None = None,
    code: str | None = None,
) -> None:
    content: list[Flowable] = [
        Callout(label, body, colors.HexColor("#2563EB")),
        Spacer(1, 6),
    ]
    if narration:
        content.append(_paragraph(f"<b>Narration:</b> “{narration}”", styles["body"]))
    if code:
        content.append(_paragraph(code, styles["code"]))
    content.append(Spacer(1, 6))
    story.append(KeepTogether(content))


def build_pdf(output_path: Path) -> None:
    """Build the professional video-submission script document."""
    styles = _styles()
    frame = Frame(
        0.7 * inch,
        0.7 * inch,
        PAGE_WIDTH - 1.4 * inch,
        PAGE_HEIGHT - 1.4 * inch,
        id="content",
    )
    document = BaseDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
    )
    document.addPageTemplates(
        [PageTemplate(id="main", frames=[frame], onPage=_page_number)]
    )

    story: list[Flowable] = [
        Spacer(1, 2.2 * inch),
        _paragraph("Autonomous Agent - Video Submission Script", styles["title"]),
        _paragraph(
            "Live Demo, Architecture, Debugging, and Tradeoffs",
            styles["subtitle"],
        ),
        Spacer(1, 0.45 * inch),
        _paragraph("Assessment: Python AI Engineer - Autonomous Agents", styles["note"]),
        Spacer(1, 0.12 * inch),
        _paragraph("Target runtime: 8-10 minutes (recommended run: ~9 minutes)", styles["note"]),
        PageBreak(),
    ]

    _section(story, styles, "RUN OF SHOW", "Keep the Entire Recording Within 8-10 Minutes")
    story.extend(
        [
            _paragraph(
                "<b>0:00-3:30 — Live Demo:</b> Run the standard request, show the "
                "downloaded document, then submit the ambiguous retreat request.",
                styles["body"],
            ),
            _paragraph(
                "<b>3:30-6:00 — What You Built:</b> Walk through orchestration, "
                "planning, executor safety, rendering, and the API boundary.",
                styles["body"],
            ),
            _paragraph(
                "<b>6:00-7:30 — Debugging Insight:</b> Explain the concrete "
                "context-auto-injection fix and prompt hardening.",
                styles["body"],
            ),
            _paragraph(
                "<b>7:30-9:00 — Tradeoffs and Close:</b> Cover autonomy, local-model "
                "latency, reflection value, and finish with the readiness checklist.",
                styles["body"],
            ),
            _paragraph(
                "<b>Recording pace:</b> Read the narration naturally, but do not read "
                "code line-by-line. Use each highlighted callout as a visual cue and "
                "keep file tours to the named function.",
                styles["body"],
            ),
        ]
    )

    _section(
        story,
        styles,
        "1. LIVE DEMO (3-4 min)",
        "End-to-End Execution &amp; Two Test Inputs",
    )
    _cue(
        story,
        styles,
        "Screen Setup",
        "Show React UI on localhost:5173 (left) and FastAPI logs on localhost:8000 (right).",
    )
    _cue(
        story,
        styles,
        "Action 1 - Standard Request",
        "Paste the logistics proposal request into the UI and click Generate.",
        "First, a standard request. The UI shows a loading spinner. Look at the FastAPI "
        "terminal: the agent is making multiple calls to the local Ollama model. It first "
        "plans the TODO list, executes the tools, and finally renders the .docx. The "
        "important point is that this is not a single text-generation call: the request "
        "moves through a visible, auditable workflow. Keep this explanation to about "
        "thirty seconds while the model is running.",
        'Create a business proposal for a mid-sized logistics company adopting AI-based '
        "route optimization...",
    )
    _cue(
        story,
        styles,
        "Action 2 - Show Output",
        "Show the completed UI summary. Click Download, open the .docx in Word, then show the title page, TOC, and populated sections.",
        "The API response gives the frontend both a natural-language summary and a "
        "download URL. In Word, quickly show the title page, the updateable table of "
        "contents, and a few populated sections. Do not scroll through every page; this "
        "should take about thirty seconds.",
    )
    _cue(
        story,
        styles,
        "Action 3 - Complex Request",
        "Paste the team-retreat project-plan request and click Generate.",
        "Now, the complex request. This tests missing information and conflicting "
        "requirements. Notice the Agent Assumptions box in the UI—the agent explicitly "
        "states it assumed a 3-day retreat and a tight-but-premium budget. This proves "
        "autonomous decision-making. It also makes uncertainty inspectable instead of "
        "silently inventing facts, which is important for business-document workflows. "
        "Spend no more than forty-five seconds on this example.",
        "We need a project plan for our team retreat next quarter. Budget is tight but we "
        "want it to feel premium. Attendance is optional but management wants 90%. We are "
        "not sure if it is 2 or 3 days...",
    )
    _cue(
        story,
        styles,
        "Action 4 - Agent Task List",
        "Show the JSON response or terminal output and highlight plan.todos with every status set to done.",
        code='"plan": { "todos": [{ "tool": "generate_outline", "status": "done" }, ...] }',
    )

    _section(
        story,
        styles,
        "2. WHAT YOU BUILT (2-3 min)",
        "Architecture, Planning Logic, Tool Orchestration, API Design, Mandatory Improvement",
    )
    _cue(
        story,
        styles,
        "File to Show",
        "app/agent/orchestrator.py - run_agent function",
        "The Orchestrator is the brain stem of the application. It is intentionally kept "
        "very small. It does four things: it asks the Planner to generate the plan, hands "
        "the plan to the Executor to run the tools, asks the Reflector to check for "
        "missing sections, and finally renders the document. We also capped the "
        "reflection to one follow-up pass, which prevents infinite loops if the model "
        "gets confused. Keeping this function thin matters because each component can be "
        "tested independently: orchestration controls sequence, while the planner, "
        "executor, and reflector each own one clear responsibility. Spend about "
        "thirty-five seconds here, then point to the next file.",
        "async def run_agent(request, ollama, request_id, session_id):\n"
        "    plan = await plan(request, ollama, context)\n"
        "    state = await executor.execute(plan)\n"
        "    reflection = await reflect(request, plan, state.results, ollama)",
    )
    _cue(
        story,
        styles,
        "File to Show",
        "app/agent/planner.py - plan function",
        "The Planner uses the qwen2.5-coder 7-billion parameter model. It outputs strict "
        "JSON. Pydantic validates the shape of this JSON. But we also added semantic "
        "repairs in Python: even if the LLM forgets, we force the plan to have an outline "
        "as step 1, and a document render as the final step. This is our Mandatory "
        "Engineering Improvement: Multi-step Planning. In other words, the model "
        "proposes the work, but deterministic Python code protects the workflow "
        "invariants that the rest of the system depends on. Keep this explanation to "
        "about thirty seconds.",
    )
    _cue(
        story,
        styles,
        "File to Show",
        "app/agent/executor.py - execute function",
        "The Executor runs the TODOs one by one using our Tool Registry. The most "
        "important feature here is argument sanitization. Small local models hallucinate "
        "arguments, so the executor strips out anything that isn't explicitly defined in "
        "the tool's schema. If a non-render tool fails, it records the error and keeps "
        "going so we still get a partial document. But if the renderer fails, it stops.",
        " This distinction is intentional: partial research or prose is still useful for "
        "review, whereas a successful run without a downloadable document would not meet "
        "the product goal. Cover this in roughly thirty-five seconds.",
    )
    _cue(
        story,
        styles,
        "File to Show",
        "app/tools/docx_renderer.py - render_docx function",
        "The Renderer uses python-docx and OxmlElement to inject a real Word TOC field, "
        "page numbers, and styled tables, ensuring the final document is polished.",
    )
    _cue(
        story,
        styles,
        "File to Show",
        "app/main.py - post_agent route",
        "The API design is clean: a single POST /agent route. Notice that the Ollama "
        "client is injected as a dependency. This is a standard software engineering "
        "pattern that keeps our endpoint logic separate from the model client state. It "
        "also means our 31 automated tests can run completely offline using a fake "
        "Ollama mock. The route itself stays intentionally thin: it validates input, "
        "starts the agent flow, and shapes the response for the React frontend. This is "
        "why the API layer remains easy to reason about and test.",
    )

    _section(
        story,
        styles,
        "3. DEBUGGING INSIGHT (1-2 min)",
        "Debugging Ability, Problem-Solving Approach",
    )
    _cue(
        story,
        styles,
        "File to Show",
        "app/agent/executor.py - context auto-injection logic",
        "The hardest bug was that the 3B and 7B models kept failing to pass the correct "
        "arguments to the tools. For example, they would call generate_section_content "
        "with just {section_type: 'executive_summary'} but miss the required doc_title "
        "and data_block.<br/><br/>The root cause was that LLMs are bad at maintaining "
        "schema state. My fix was to "
        "build a 'Context Auto-Injection' pattern. The executor ignores whatever arguments "
        "the LLM passes for these specific tools and constructs the dictionary from scratch "
        "using the plan metadata.",
        'if todo.tool == "generate_section_content":\n'
        '    args = {"doc_type": plan.doc_type.value, "doc_title": plan.title,\n'
        '            "section_title": section_title, "data_block": data_block,\n'
        '            "ollama": self._ollama}',
    )
    _cue(
        story,
        styles,
        "File to Show",
        "app/llm/prompts.py - planner_system_prompt",
        "I also updated the prompt to explicitly ban hallucinated tools like add_table. "
        "The result is a resilient system that handles bad model outputs gracefully "
        "without crashing.",
    )

    _section(
        story,
        styles,
        "4. TRADEOFF DISCUSSION (1-2 min)",
        "Scalability, Architecture Thinking",
    )
    _cue(
        story,
        styles,
        "File to Show",
        "app/main.py - dependency injection",
        "Tradeoff 1: Autonomous Planning vs Deterministic Workflows. We chose autonomous "
        "planning—the LLM creates the TODO list. This is flexible but risky. We mitigated "
        "the risk with the Reflection stage and the executor's fallback logic. For a "
        "production system, this boundary is explicit: more reliability could come from "
        "tighter templates, but at the cost of flexibility. The current design makes "
        "that choice visible rather than hiding it: every generated plan is returned to "
        "the client for transparency.",
    )
    _cue(
        story,
        styles,
        "Narration",
        "The second major tradeoff is Speed versus Functionality. We chose local Ollama "
        "models to avoid API costs and ensure data privacy. The tradeoff is that they are "
        "slow. A document takes 2 to 5 minutes. To offset this, we built the FastAPI "
        "backend with async endpoints, so the server can handle other requests while "
        "Ollama works in the background. It's a deliberate choice: we accepted higher "
        "latency for zero cost and full privacy. For this application, document quality "
        "and keeping business data local were more important than instant response time. "
        "Keep the explanation concise—about twenty-five seconds—while the server remains "
        "visible.",
    )
    _cue(
        story,
        styles,
        "File to Show",
        "app/agent/reflector.py - reflect function",
        "Tradeoff 3: Multi-step planning adds latency because of the extra LLM calls for "
        "reflection. But it significantly improves coverage—the agent catches missing "
        "sections and retries them. The one-pass cap is the practical compromise: it "
        "improves quality without risking an expensive reflection loop. This gives the "
        "agent one chance to self-correct, while preserving a predictable upper bound on "
        "latency and model usage.",
    )

    _section(story, styles, "5. FINAL CHECKLIST", "Recording Readiness")
    for item in [
        "Delete old output files before recording.",
        "Start uvicorn app.main:app --reload in Terminal 1.",
        "Start npm run dev in frontend (Terminal 2).",
        "Have Word open and ready.",
    ]:
        story.append(_paragraph(f"• {item}", styles["body"]))

    document.build(story)


if __name__ == "__main__":
    build_pdf(OUTPUT_PATH)
    print(f"Generated {OUTPUT_PATH.resolve()}")
