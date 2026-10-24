import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import main


class ConfigurationTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        directory = self.enterContext(tempfile.TemporaryDirectory())
        self.directory = Path(directory)
        self.enterContext(patch.object(main, "__file__", str(self.directory / "main.py")))
        self.enterContext(patch.dict(os.environ, {}, clear=True))
        self.configure_key = self.enterContext(patch.object(main, "set_default_openai_key"))
        self.run_agent = self.enterContext(
            patch.object(main.Runner, "run", new_callable=AsyncMock)
        )
        self.run_agent.return_value = SimpleNamespace(final_output="Resultado de prueba")
        self.enterContext(patch("builtins.print"))

    async def test_dotenv_key_is_configured_before_agent_runs(self) -> None:
        (self.directory / ".env").write_text(
            "OPENAI_API_KEY=test-only-dotenv-value\n", encoding="utf-8"
        )

        async def check_configuration(*args: object, **kwargs: object) -> SimpleNamespace:
            self.configure_key.assert_called_once_with("test-only-dotenv-value")
            return SimpleNamespace(final_output="Resultado de prueba")

        self.run_agent.side_effect = check_configuration
        await main.main()
        self.run_agent.assert_awaited_once()

    async def test_environment_takes_precedence_over_dotenv(self) -> None:
        os.environ["OPENAI_API_KEY"] = "test-only-environment-value"
        (self.directory / ".env").write_text(
            "OPENAI_API_KEY=test-only-dotenv-value\n", encoding="utf-8"
        )
        await main.main()
        self.configure_key.assert_called_once_with("test-only-environment-value")
        self.run_agent.assert_awaited_once()

    async def test_missing_key_stops_before_agent_runs(self) -> None:
        with self.assertRaisesRegex(SystemExit, "Falta OPENAI_API_KEY"):
            await main.main()
        self.configure_key.assert_not_called()
        self.run_agent.assert_not_awaited()

    async def test_empty_environment_key_does_not_fall_back_to_dotenv(self) -> None:
        (self.directory / ".env").write_text(
            "OPENAI_API_KEY=test-only-dotenv-value\n", encoding="utf-8"
        )
        for value in ("", "   "):
            with self.subTest(value=value):
                os.environ["OPENAI_API_KEY"] = value
                with self.assertRaisesRegex(SystemExit, "Falta OPENAI_API_KEY"):
                    await main.main()
                self.configure_key.assert_not_called()
                self.run_agent.assert_not_awaited()
