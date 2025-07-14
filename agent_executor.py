from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
import json
from test_client import get_agent_answer

class OCIAllRealmFinderAgent:
    """Finds the OCI functioning realms and their status, and calls another agent."""

    def __init__(self):
        # URL of the other agent to call (update as needed)
        self.other_agent_url = "http://localhost:9998"

    async def invoke(self) -> dict:
        # Use the shared get_agent_answer function to call the other agent
        other_agent_result = await get_agent_answer(self.other_agent_url, "What is the status of OC1, OC2, OC3?")
        this_agent_result = '🟩 New Realms Status 🟩: OC4 ✅, OC5 ✅, OC6 ✅'
        return {
            "this_agent_result": this_agent_result,
            "other_agent_result": other_agent_result
        }

class OCIAllRealmFinderAgentExecutor(AgentExecutor):
    """Test AgentProxy Implementation that delegates to the agent's invoke method."""

    def __init__(self):
        self.agent = OCIAllRealmFinderAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        result = await self.agent.invoke()
        # Serialize the result dict for output, preserving Unicode (emojis)
        await event_queue.enqueue_event(new_agent_text_message(json.dumps(result, indent=2, ensure_ascii=False)))

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')


