"""
autonomy_tools.py - MCP tools for autonomous goal tracking and self-correction.

These tools allow the AI agent to register long-term goals and analyze
errors in order to suggest corrective strategies at runtime.
"""
import json
import time
from src.utils.logging_config import logger

# In-memory store for goals and error history.
# For persistence across sessions, replace with a database or file backend.
_goals: dict[str, dict] = {}
_error_log: list[dict] = []


def register(mcp):

    @mcp.tool()
    def register_autonomous_goal(goal: str, priority: int = 1) -> str:
        """
        Register a long-term goal for the agent to pursue autonomously.

        Args:
            goal:     Natural language description of the goal.
            priority: Integer priority level (1 = low, 5 = critical). Defaults to 1.

        Returns:
            Confirmation with the assigned goal ID.
        """
        goal_id = f"goal_{int(time.time() * 1000)}"
        _goals[goal_id] = {
            "id": goal_id,
            "goal": goal,
            "priority": priority,
            "status": "active",
            "registered_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        logger.info("Goal registered: id=%s priority=%d goal=%s", goal_id, priority, goal)
        return f"Goal registered. id={goal_id} priority={priority}"

    @mcp.tool()
    def list_autonomous_goals() -> str:
        """
        Return all registered goals and their current status.

        Returns:
            JSON-serialized list of goal objects.
        """
        goals = list(_goals.values())
        logger.info("Listing %d registered goals.", len(goals))
        return json.dumps(goals, indent=2)

    @mcp.tool()
    def complete_goal(goal_id: str) -> str:
        """
        Mark a registered goal as completed.

        Args:
            goal_id: The ID returned by register_autonomous_goal.

        Returns:
            Confirmation or an error if the goal was not found.
        """
        if goal_id not in _goals:
            return f"Goal not found: {goal_id}"
        _goals[goal_id]["status"] = "completed"
        logger.info("Goal marked as completed: %s", goal_id)
        return f"Goal {goal_id} marked as completed."

    @mcp.tool()
    def run_self_correction(task_id: str, error: str) -> str:
        """
        Analyze a task error and suggest a corrective strategy.

        Args:
            task_id: Identifier for the task that produced the error.
            error:   Error message or description.

        Returns:
            Suggested corrective action as a string.
        """
        entry = {
            "task_id": task_id,
            "error": error,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        _error_log.append(entry)
        logger.warning("Self-correction triggered for task=%s error=%s", task_id, error)

        # Heuristic strategy selector - extend with real logic as needed.
        error_lower = error.lower()
        if "timeout" in error_lower:
            strategy = "Retry with exponential backoff. Consider increasing the timeout threshold."
        elif "permission" in error_lower or "unauthorized" in error_lower:
            strategy = "Verify credentials and permission scopes before retrying."
        elif "not found" in error_lower or "404" in error_lower:
            strategy = "Validate the target resource path or identifier before retrying."
        elif "syntax" in error_lower:
            strategy = "Review the generated code or query for syntax errors and regenerate."
        else:
            strategy = "Log the error, isolate the failing step, and retry with a simplified input."

        return f"Self-correction analysis for task '{task_id}': {strategy}"
