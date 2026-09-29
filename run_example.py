"""Run the legal matter handoff against Infrai."""
from legal_workflow import MatterIntake, run_workflow


if __name__ == "__main__":
    matter = MatterIntake(
        matter_id="matter-104",
        client_name="Jordan Lee",
        summary="Review settlement agreement and send the signed copy.",
        deadline_days=5,
    )
    print(run_workflow(matter))

