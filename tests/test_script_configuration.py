import os
import runpy
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

SCRIPT_NAMES = (
    "carga de openai_api_key.py",
    "uso de tokens.py",
    "image analizer.py",
)
SOURCE_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


class ScriptConfigurationTests(unittest.TestCase):
    def setUp(self) -> None:
        project = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.project = project
        scripts = project / "scripts"
        scripts.mkdir()
        for name in SCRIPT_NAMES:
            shutil.copyfile(SOURCE_SCRIPTS / name, scripts / name)
        self.enterContext(patch.dict(os.environ, {}, clear=True))
        self.client = self.enterContext(patch("openai.OpenAI"))
        self.enterContext(patch("builtins.print"))
        self.client.return_value.responses.create.return_value = SimpleNamespace(
            output_text="Resultado de prueba",
            usage=SimpleNamespace(input_tokens=12, output_tokens=8, total_tokens=20),
        )

    def run_each_script(self, expected_key: str) -> None:
        for name in SCRIPT_NAMES:
            with self.subTest(script=name):
                self.client.reset_mock()
                runpy.run_path(str(self.project / "scripts" / name), run_name="__main__")
                self.client.assert_called_once_with(api_key=expected_key)

    def test_all_scripts_load_key_from_project_root(self) -> None:
        (self.project / ".env").write_text(
            "OPENAI_API_KEY=test-only-root-value\n", encoding="utf-8"
        )
        self.run_each_script("test-only-root-value")

    def test_environment_key_takes_precedence(self) -> None:
        os.environ["OPENAI_API_KEY"] = "test-only-environment-value"
        (self.project / ".env").write_text(
            "OPENAI_API_KEY=test-only-root-value\n", encoding="utf-8"
        )
        self.run_each_script("test-only-environment-value")

    def test_missing_key_stops_before_client_creation(self) -> None:
        for name in SCRIPT_NAMES:
            with self.subTest(script=name):
                self.client.reset_mock()
                with self.assertRaisesRegex(SystemExit, "Falta OPENAI_API_KEY"):
                    runpy.run_path(str(self.project / "scripts" / name), run_name="__main__")
                self.client.assert_not_called()

    def test_blank_environment_key_is_rejected(self) -> None:
        (self.project / ".env").write_text(
            "OPENAI_API_KEY=test-only-root-value\n", encoding="utf-8"
        )
        for value in ("", "   "):
            os.environ["OPENAI_API_KEY"] = value
            for name in SCRIPT_NAMES:
                with self.subTest(script=name, value=value):
                    self.client.reset_mock()
                    with self.assertRaisesRegex(SystemExit, "Falta OPENAI_API_KEY"):
                        runpy.run_path(str(self.project / "scripts" / name), run_name="__main__")
                    self.client.assert_not_called()
