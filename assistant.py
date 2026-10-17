import inspect
from tool_registry import TOOLS


def execute(result):
    """
    Executes a tool selected by the brain with flexible argument support.
    """
    if not isinstance(result, dict):
        return f"Invalid action format: {result}"

    tool_name = result.get("tool")

    if tool_name == "unknown":
        return f"I couldn't understand: {result.get('raw', 'unknown command')}"

    if not tool_name or tool_name not in TOOLS:
        return f"Unknown tool: {tool_name}"

    tool_info = TOOLS[tool_name]
    func = tool_info["function"]

    # Gather arguments: prefer 'arguments' dict, otherwise gather top-level keys
    args = result.get("arguments")
    if args is None:
        args = {k: v for k, v in result.items() if k not in ["tool", "type", "raw"]}

    try:
        # If args is a dictionary, pass as keyword arguments matching function signature
        if isinstance(args, dict):
            sig = inspect.signature(func)
            valid_args = {}
            for param_name in sig.parameters.keys():
                if param_name in args:
                    valid_args[param_name] = args[param_name]
                # Map common fallback aliases
                elif param_name == "song" and "song_name" in args:
                    valid_args[param_name] = args["song_name"]
                elif param_name == "query" and "search_query" in args:
                    valid_args[param_name] = args["search_query"]
                elif param_name == "app_name" and "app" in args:
                    valid_args[param_name] = args["app"]
                elif param_name == "folder_name" and "folder" in args:
                    valid_args[param_name] = args["folder"]
                elif param_name == "file_name" and "file" in args:
                    valid_args[param_name] = args["file"]

            # If function has parameters and valid_args has them, call with kwargs
            if valid_args:
                return func(**valid_args)
            elif len(args) == 1:
                # If only one argument was provided, pass its value directly
                first_val = next(iter(args.values()))
                return func(first_val)
            else:
                return func()
        elif isinstance(args, (list, tuple)):
            return func(*args)
        else:
            return func(args)
    except Exception as e:
        print(f"❌ Error executing {tool_name}: {e}")
        return f"Failed to execute {tool_name}: {e}"