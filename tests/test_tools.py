import json
import os
import runpy
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "tools.py"


class ToolCallingTests(unittest.TestCase):
    def test_get_weather_is_explicitly_simulated(self) -> None:
        module = runpy.run_path(str(SCRIPT_PATH), run_name="tools_example")

        result = module["get_weather"]("Paris, France")

        self.assertEqual(result["location"], "Paris, France")
        self.assertEqual(result["temperature"], 18)
        self.assertTrue(result["simulated"])

    def test_function_result_is_sent_back_with_matching_call_id(self) -> None:
        project = Path(self.enterContext(tempfile.TemporaryDirectory()))
        scripts = project / "scripts"
        scripts.mkdir()
        shutil.copyfile(SCRIPT_PATH, scripts / "tools.py")
        (project / ".env").write_text(
            "OPENAI_API_KEY=test-only-root-value\n", encoding="utf-8"
        )

        tool_call = SimpleNamespace(
            type="function_call",
            name="get_weather",
            arguments='{"location":"Paris, France"}',
            call_id="call_test",
        )
        first_response = SimpleNamespace(
            id="response_test", output=[tool_call], output_text=""
        )
        final_response = SimpleNamespace(output_text="Dato simulado para París.")

        with (
            patch.dict(os.environ, {}, clear=True),
            patch("openai.OpenAI") as client,
            patch("builtins.print") as output,
        ):
            client.return_value.responses.create.side_effect = [
                first_response,
                final_response,
            ]
            runpy.run_path(str(scripts / "tools.py"), run_name="__main__")

        client.assert_called_once_with(api_key="test-only-root-value")
        self.assertEqual(client.return_value.responses.create.call_count, 2)
        first_request = client.return_value.responses.create.call_args_list[0].kwargs
        self.assertEqual(
            first_request["tool_choice"],
            {"type": "function", "name": "get_weather"},
        )
        second_request = client.return_value.responses.create.call_args_list[1].kwargs
        self.assertEqual(second_request["previous_response_id"], "response_test")
        self.assertEqual(second_request["input"][0]["call_id"], "call_test")
        self.assertEqual(second_request["input"][0]["type"], "function_call_output")
        self.assertTrue(json.loads(second_request["input"][0]["output"])["simulated"])
        output.assert_called_once_with("Dato simulado para París.")
