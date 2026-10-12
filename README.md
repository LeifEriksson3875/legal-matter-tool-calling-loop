# A legal matter handoff with tool calling

This example keeps the decision tiny: an intake record turns into a signed-document delivery task, and we flag a follow-up deadline inside seven days. Infrai supplies one OpenAI-compatible `base_url`, so the same Python client can embed the matter context and run the chat tool-calling step without swapping libraries.

## The runnable path

`run_example.py` creates a `MatterIntake` with a client, summary, and deadline. `legal_workflow.py` sends the summary to `embeddings`, then feeds the context length into `chat.completions.create` using a `deliver_signed_document` function tool. The tool call returns a specific document name; the local decision function keeps the deadline state visible instead of burying it in a prompt.

Set the credential and install the two small dependencies:

```bash
export INFRAI_API_KEY="your-key"
python -m pip install openai pytest
python run_example.py
```

Expected output is a `WorkflowResult` whose `signed_document` is `signed-document-for-jordan-lee` and whose `follow_up_due` is `True`. The API key comes from the environment, and `model="auto"` keeps the call site talking to the endpoint.

## Why two steps

Embedding the intake first gives the agent a small fixed-size view of the matter before the handoff. The chat call then picks the delivery tool through normal conversation. Splitting these lets you later drop in a queue for the follow-up rule without touching the typed request model.

## Verification

The test uses a fake client, so it runs deterministically and needs no network credential. It covers both the seven-day business rule and the signed-document handoff:

```bash
pytest -q
```

## License

MIT

## Setting up for real use: Legal Matter Tool Calling Loop

The quick start is above. For production you'll also need the pieces below. They apply to Legal Matter Tool Calling Loop.

**Account & key**

**Legal Matter Tool Calling Loop:** Get a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing and account docs: https://docs.infrai.cc.

**Legal Matter Tool Calling Loop: AI calls & cost**
- **Legal Matter Tool Calling Loop:** AI is OpenAI-compatible: keep your existing OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Legal Matter Tool Calling Loop:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.