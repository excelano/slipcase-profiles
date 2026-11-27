# Author: David M. Anderson
# Built with AI assistance (Claude, Anthropic)

import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest

TOOLS = pathlib.Path(__file__).parent
REPO = TOOLS.parent
EXAMPLES = REPO / "records" / "examples"


def run(tool: str, *args) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOLS / tool), *map(str, args)],
        capture_output=True,
        text=True,
    )


def record(case: pathlib.Path) -> tuple[str, str]:
    doc = tomllib.loads((case / "slipcase.flyleaf.toml").read_text())
    return doc["records"]["id"], doc["records"]["events_head"]


class VerifyLog(unittest.TestCase):
    def test_the_conventions_example_is_intact(self):
        got = run("verify-log.py", REPO / "examples" / "conventions" / "events.toml",
                  "event", "01927c3e-8b2a-7d41-9f3c-2a6e5b1c4d7f")
        self.assertEqual(got.returncode, 0, got.stderr)
        self.assertTrue(got.stdout.startswith("intact: 2 entries"), got.stdout)

    def test_every_valid_record_log_hashes_to_its_head(self):
        for case in sorted((EXAMPLES / "valid").iterdir()):
            log = case / "records" / "events.toml"
            if not log.exists():
                continue
            seed, head = record(case)
            with self.subTest(case.name):
                got = run("verify-log.py", log, "event", seed, head)
                self.assertEqual(got.returncode, 0, got.stderr)

    def test_each_broken_chain_is_refused(self):
        cases = {
            "events-chain-broken": "broken at entry",
            "events-wrong-seed": "broken at entry 1",
            "events-head-wrong": "recorded head",
            "events-crlf": "CR",
        }
        for name, said in cases.items():
            case = EXAMPLES / "invalid" / name
            seed, head = record(case)
            with self.subTest(name):
                got = run("verify-log.py", case / "records" / "events.toml", "event", seed, head)
                self.assertNotEqual(got.returncode, 0)
                self.assertIn(said, got.stderr)


class VerifyRegister(unittest.TestCase):
    def test_the_example_register_is_intact_with_one_unfinished_intent(self):
        got = run("verify-register.py", EXAMPLES / "register")
        self.assertEqual(got.returncode, 0, got.stderr)
        self.assertIn("000001: final", got.stdout)
        self.assertIn("000002: unfinished intent", got.stdout)
        self.assertTrue(got.stdout.endswith("chain intact\n"), got.stdout)

    def test_a_changed_journal_breaks_the_chain(self):
        with tempfile.TemporaryDirectory() as dir:
            register = pathlib.Path(dir) / "register"
            shutil.copytree(EXAMPLES / "register", register)
            with open(register / "000001.journal", "ab") as journal:
                journal.write(b"\n")
            got = run("verify-register.py", register)
            self.assertNotEqual(got.returncode, 0)
            self.assertIn("broken at 000001: journal_sha256 does not match", got.stderr)

    def test_a_missing_intent_is_a_gap(self):
        with tempfile.TemporaryDirectory() as dir:
            register = pathlib.Path(dir) / "register"
            shutil.copytree(EXAMPLES / "register", register)
            shutil.copytree(register / "000002.intent.slpc", register / "000003.intent.slpc")
            shutil.rmtree(register / "000002.intent.slpc")
            got = run("verify-register.py", register)
            self.assertIn("broken at 000002: no intent", got.stderr)

    def test_a_directory_without_intents_is_not_a_register(self):
        with tempfile.TemporaryDirectory() as dir:
            got = run("verify-register.py", dir)
            self.assertIn("not a register", got.stderr)


class CheckCore(unittest.TestCase):
    def test_every_case_reaches_its_verdict(self):
        cases = REPO / "core" / "examples"
        manifest = tomllib.loads((cases / "manifest.toml").read_text())
        for case in manifest["case"]:
            with self.subTest(case["name"]):
                folder = "valid" if case["verdict"] == "conformant" else "invalid"
                got = run("check-core.py", cases / folder / case["name"])
                if case["verdict"] == "conformant":
                    self.assertEqual(got.returncode, 0, got.stdout + got.stderr)
                    self.assertEqual(got.stdout.strip(), "conformant")
                else:
                    self.assertEqual(got.returncode, 1, got.stdout + got.stderr)
                    self.assertTrue(
                        got.stdout.startswith(f"non-conformant {case['rule']}:"),
                        got.stdout,
                    )

    def test_the_word_fixture_maps_as_section_4_says(self):
        import datetime
        import xml.etree.ElementTree as ET

        ns = {
            "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcterms": "http://purl.org/dc/terms/",
        }
        examples = REPO / "core" / "examples"
        props = ET.parse(examples / "fixtures" / "word-core.xml").getroot()

        def text(tag):
            return props.find(tag, ns).text.strip()

        core = tomllib.loads(
            (examples / "valid" / "from-word" / "slipcase.flyleaf.toml").read_text()
        )["core"]
        created = datetime.datetime.fromisoformat(text("dcterms:created"))

        self.assertEqual(core["title"], text("dc:title"))
        self.assertEqual(core["creator"], [{"name": text("dc:creator")}])
        self.assertIn(";", text("dc:creator"))
        self.assertEqual(core["subject"], [text("dc:subject")])
        self.assertTrue(text("cp:keywords"))
        self.assertEqual(core["description"], text("dc:description"))
        self.assertEqual(core["created"], created.astimezone(datetime.timezone.utc).date())
        self.assertNotEqual(core["created"], created.astimezone(datetime.timezone(datetime.timedelta(hours=-6))).date())
        self.assertEqual(set(core) - {"profile", "profile_version", "kind"},
                         {"title", "creator", "subject", "description", "created", "modified"})

    def test_a_missing_case_is_a_usage_error(self):
        self.assertEqual(run("check-core.py", REPO / "no-such-case").returncode, 2)


class CheckSchedule(unittest.TestCase):
    def test_each_schedule_example_reaches_its_verdict(self):
        schedules = EXAMPLES / "schedule"
        manifest = tomllib.loads((schedules / "manifest.toml").read_text())
        for case in manifest["case"]:
            with self.subTest(case["file"]):
                got = run("check-schedule.py", schedules / case["file"])
                if case["verdict"] == "loads":
                    self.assertEqual(got.returncode, 0, got.stdout + got.stderr)
                    self.assertTrue(got.stdout.startswith("loaded "), got.stdout)
                else:
                    self.assertEqual(got.returncode, 1, got.stdout + got.stderr)
                    self.assertTrue(got.stdout.startswith("row "), got.stdout)

    def test_the_nara_fixture_loads_all_its_rows(self):
        got = run("check-schedule.py", EXAMPLES / "schedule" / "grs-transmittal36.csv")
        self.assertTrue(got.stdout.startswith("loaded 308 rows"), got.stdout)


if __name__ == "__main__":
    unittest.main()
