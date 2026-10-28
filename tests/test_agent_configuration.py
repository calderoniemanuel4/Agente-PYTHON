import os
import runpy
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from agents import Runner


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "agent.py"


class AgentConfigurationTests(unittest.TestCase):
    def setUp(self) -> None:
        project = Path(self.enterContext(tempfile.TemporaryDirectory()))
        scripts = project / "scripts"
        scripts.mkdir()
        self.script = scripts / "agent.py"
        shutil.copyfile(SCRIPT_PATH, self.script)
        self.project = project
        self.enterContext(patch.dict(os.environ, {}, clear=True))
        self.set_key = self.enterContext(patch("agents.set_default_openai_key"))
        self.run_agent = self.enterContext(
            patch.object(Runner, "run", new_callable=AsyncMock)
        )
        self.enterContext(patch("builtins.print"))

    def test_root_dotenv_key_is_configured_before_run(self) -> None:
        (self.project / ".env").write_text(
            "OPENAI_API_KEY=test-only-root-value\n", encoding="utf-8"
        )

        async def check_key(*args: object, **kwargs: object) -> SimpleNamespace:
            self.set_key.assert_called_once_with("test-only-root-value")
            return SimpleNamespace(final_output="Resultado de prueba")

        self.run_agent.side_effect = check_key
        runpy.run_path(str(self.script), run_name="__main__")
        self.run_agent.assert_awaited_once()

    def test_missing_key_stops_before_run(self) -> None:
        with self.assertRaisesRegex(SystemExit, "Falta OPENAI_API_KEY"):
            runpy.run_path(str(self.script), run_name="__main__")
        self.set_key.assert_not_called()
        self.run_agent.assert_not_awaited()
