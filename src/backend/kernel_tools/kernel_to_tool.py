from azure.ai.agents.models import ToolDefinition, AgentsResponseFormat
from semantic_kernel.functions.kernel_function import KernelFunction
from typing import Optional

class KernelFunctionToolWrapper(ToolDefinition):
    def __init__(
        self,
        kernel_function: KernelFunction,
        name: Optional[str] = None,
        description: Optional[str] = None
    ):
        self._kernel_function = kernel_function
        self.name = name or kernel_function.name
        self.description = description or kernel_function.description or "SK-wrapped function"

    async def invoke(self, request) -> AgentsResponseFormat:
        args = request.args or {}
        input_value = args.get("input", "")
        result = await self._kernel_function.invoke_async(input_value)
        return AgentsResponseFormat(output=result if isinstance(result, str) else str(result))#AgentsResponseFormat(output=str(result))

    @property
    def _data(self) -> dict:
        """Required for Azure Agent framework and planner compatibility."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string",
                        "description": "Input string for the function"
                    }
                },
                "required": ["input"]
            }
        }


def create_tool_from_kernel_function(
    kernel_function: KernelFunction,
    name: Optional[str] = None,
    description: Optional[str] = None
) -> ToolDefinition:
    return KernelFunctionToolWrapper(kernel_function, name, description)
