"""Template 8: Executive Function Agent."""

from __future__ import annotations

from typing import Any

from cynthia.base import Agent


class ExecutiveFunctionAgent(Agent):
    """Plan, prioritize, and coordinate all other agents.

    Inputs: all agent outputs
    Outputs: task schedule, coordination commands
    Key params: priority_rules, oversight_scope
    """

    role = "executive_function"

    def __init__(
        self,
        name: str | None = None,
        priority_rules: tuple[str, ...] = (),
        oversight_scope: tuple[str, ...] = (),
        **params: Any,
    ) -> None:
        super().__init__(
            name,
            priority_rules=priority_rules,
            oversight_scope=oversight_scope,
            **params,
        )

    def process(self, agent_outputs: dict[str, Any]) -> dict[str, Any]:
        """Turn a map of ``{role: latest_output}`` into a prioritized task schedule.

        Only roles listed in ``oversight_scope`` are coordinated (all roles,
        if ``oversight_scope`` is empty). Roles in ``priority_rules`` are
        scheduled first, in the order given.
        """
        scope = self.params["oversight_scope"]
        in_scope = {r: v for r, v in agent_outputs.items() if not scope or r in scope}

        priority_rules = self.params["priority_rules"]
        ordered = [r for r in priority_rules if r in in_scope]
        ordered += sorted(r for r in in_scope if r not in priority_rules)

        return {
            "schedule": ordered,
            "commands": {role: in_scope[role] for role in ordered},
        }
