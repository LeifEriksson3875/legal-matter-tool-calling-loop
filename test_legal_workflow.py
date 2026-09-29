from types import SimpleNamespace

from legal_workflow import MatterIntake, follow_up_needed, run_workflow


class FakeChat:
    def completions(self):
        return self

    def create(self, **kwargs: object):
        messages = kwargs["messages"]
        assert isinstance(messages, list)
        assert "Jordan Lee" in messages[-1]["content"]
        tools = kwargs["tools"]
        assert isinstance(tools, list)
        assert "client_name" in tools[0]["function"]["parameters"]["required"]
        call = SimpleNamespace(function=SimpleNamespace(name="deliver_signed_document"))
        message = SimpleNamespace(content="handoff complete", tool_calls=[SimpleNamespace(function=call.function)])
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


class FakeClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=FakeChat().create))


def test_deadline_decision_and_signed_delivery():
    matter = MatterIntake("m-1", "Jordan Lee", "Send executed agreement", 5)
    result = run_workflow(matter, client=FakeClient(), embed=lambda _: [0.1, 0.2])
    assert follow_up_needed(5) is True
    assert result.follow_up_due is True
    assert result.signed_document == "signed-document-for-jordan-lee"
