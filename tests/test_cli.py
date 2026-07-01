import subprocess
import sys


def _python_executable() -> str:
    return sys.executable


def test_cli_runs_default_config():
    result = subprocess.run(
        [
            "c:\\Users\\SOURABI\\Downloads\\CandidateSync\\CandidateSync\\.venv311\\Scripts\\python.exe",
            "-m",
            "src.cli.main",
            "--csv",
            "input/sample_candidates.csv",
            "--resume",
            "input/resume.txt",
            "--config",
            "config/default_config.json",
        ],
        cwd="c:\\Users\\SOURABI\\Downloads\\CandidateSync\\CandidateSync",
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "DEFAULT OUTPUT" in result.stdout
    assert '{\n  "candidate_id"' in result.stdout
    assert '"full_name"' in result.stdout
    assert "Finished Successfully" in result.stdout


def test_cli_runs_custom_config():
    result = subprocess.run(
        [
            "c:\\Users\\SOURABI\\Downloads\\CandidateSync\\CandidateSync\\.venv311\\Scripts\\python.exe",
            "-m",
            "src.cli.main",
            "--csv",
            "input/sample_candidates.csv",
            "--resume",
            "input/resume.txt",
            "--config",
            "config/custom_minimal_config.json",
        ],
        cwd="c:\\Users\\SOURABI\\Downloads\\CandidateSync\\CandidateSync",
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "CUSTOM OUTPUT" in result.stdout
    assert '{\n  "candidate_name"' in result.stdout
    assert '"primary_email"' in result.stdout
