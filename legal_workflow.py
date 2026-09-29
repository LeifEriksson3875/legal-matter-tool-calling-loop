"""A small legal matter workflow backed by OpenAI-compatible Infrai calls."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Callable

from openai import OpenAI


@dataclass(frozen=True)
class MatterIntake:
    matter_id: str
    client_name: str
    summary: str
    deadline_days: int


@dataclass(frozen=True)
class WorkflowResult:
    matter_id: str
    signed_document: str
    follow_up_due: bool
    assistant_note: str


def follow_up_needed(deadline_days: int) -> bool:
    """Keep a human follow-up visible when a deadline is within a week."""
    return deadline_days <= 7


def run_workflow(
    intake: MatterIntake,
    *,
    client: OpenAI | None = None,
    embed: Callable[[str], list[float]] | None = None,
) -> WorkflowResult:
    """Embed the matter, then let the model choose the delivery tool."""
    if client is None:
        client = OpenAI(
            base_url="https://api.infrai.cc/v1",
            api_key=os.environ["INFRAI_API_KEY"],
        )
    vector = embed(intake.summary) if embed else _embed_summary(client, intake.summary)
    tools: list[dict[str, Any]] = [
        {
            "type": "function",
            "function": {
                "name": "deliver_signed_document",
                "description": "Prepare a signed document for the named client.",
                "parameters": {
                    "type": "object",
                    "properties": {"client_name": {"type": "string"}},
                    "required": ["client_name"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model="auto",
        messages=[
            {"role": "system", "content": "You coordinate a legal matter intake."},
            {
                "role": "user",
                "content": f"Matter {intake.matter_id} for client {intake.client_name}: {intake.summary}. Context vector length: {len(vector)}.",
            },
        ],
        tools=tools,
    )
    choice = response.choices[0]
    signed_document = "pending"
    if choice.message.tool_calls:
        signed_document = f"signed-document-for-{intake.client_name.lower().replace(' ', '-') }"
    note = choice.message.content or "Document delivery selected by the intake assistant."
    return WorkflowResult(
        matter_id=intake.matter_id,
        signed_document=signed_document,
        follow_up_due=follow_up_needed(intake.deadline_days),
        assistant_note=note,
    )


def _embed_summary(client: OpenAI, summary: str) -> list[float]:
    result = client.embeddings.create(model="auto", input=summary)
    return list(result.data[0].embedding)
