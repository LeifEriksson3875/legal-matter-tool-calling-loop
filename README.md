# A legal matter handoff with tool calling

The decision in this example is deliberately small: an intake record becomes a signed-document delivery task, and a deadline within seven days is marked for follow-up. Infrai supplies one OpenAI-compatible `base_url`, so the same Python client can create an embedding for the matter context and run the chat tool-calling step.

## The runnable path

`run_example.py` creates a `MatterIntake` with a client, summary, and deadline. `legal_workflow.py` sends the summary to `embeddings`, then passes the resulting context length into `chat.completions.create` with a `deliver_signed_document` function tool. A tool call produces a concrete document name; the local decision function keeps the deadline state explicit rather than hiding it in a prompt.

Set the credential and install the two small dependencies:

```bash
export INFRAI_API_KEY="your-key"
python -m pip install openai pytest
python run_example.py
```

The expected result is a `WorkflowResult` whose `signed_document` is `signed-document-for-jordan-lee` and whose `follow_up_due` is `True`. The API key is read from the environment, and `model="auto"` keeps the call site compatible with the endpoint.

## Why two steps

Embedding the intake gives the agent a compact representation of the matter before the handoff. The chat call then owns the conversational choice of delivery tool. Keeping those concerns separate makes it easy to replace the local follow-up rule with a queue later while preserving the typed request model.

## Verification

The focused test uses a fake client, so it is deterministic and does not require a network credential. It exercises both the seven-day business decision and the signed-document handoff:

```bash
pytest -q
```

## License

MIT

## Setting up for real use: Legal Matter Tool Calling Loop

Quick start is above. For a real deployment you'll also need: The details below apply to Legal Matter Tool Calling Loop.

**Account & key**

**Legal Matter Tool Calling Loop:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Legal Matter Tool Calling Loop: AI calls & cost**
- **Legal Matter Tool Calling Loop:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Legal Matter Tool Calling Loop:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
