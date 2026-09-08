"""Best-effort environment snapshots that contextualize experimental evidence."""

from __future__ import annotations

import os
import platform
import subprocess
import tomllib
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path

import numpy as np

from pqc.errors import PQCError


@dataclass(frozen=True, slots=True)
class ExperimentEnvironment:
    python_version: str
    python_implementation: str
    numpy_version: str
    liboqs_python_version: str | None
    liboqs_version: str | None
    cryptography_version: str | None
    quantumsec_version: str | None
    os: str
    os_release: str
    os_version: str
    machine_architecture: str
    cpu_identifier: str | None
    git_commit_sha: str | None
    git_worktree_dirty: bool | None

    @classmethod
    def capture(cls) -> ExperimentEnvironment:
        liboqs_version: str | None = None
        liboqs_python_version = _distribution_version("liboqs-python")
        try:
            from pqc.backends.oqs_backend import oqs_runtime_versions

            versions = oqs_runtime_versions()
            liboqs_version = versions.liboqs
            liboqs_python_version = versions.liboqs_python
        except ImportError, OSError, RuntimeError, PQCError:
            pass
        cpu = platform.processor().strip() or os.environ.get("PROCESSOR_IDENTIFIER", "").strip()
        git_commit_sha, git_worktree_dirty = _git_state()
        return cls(
            python_version=platform.python_version(),
            python_implementation=platform.python_implementation(),
            numpy_version=np.__version__,
            liboqs_python_version=liboqs_python_version,
            liboqs_version=liboqs_version,
            cryptography_version=_distribution_version("cryptography"),
            quantumsec_version=_quantumsec_version(),
            os=platform.system(),
            os_release=platform.release(),
            os_version=platform.version(),
            machine_architecture=platform.machine(),
            cpu_identifier=cpu or None,
            git_commit_sha=git_commit_sha,
            git_worktree_dirty=git_worktree_dirty,
        )

    def to_public_dict(self) -> dict[str, object]:
        return {
            "python_version": self.python_version,
            "python_implementation": self.python_implementation,
            "numpy_version": self.numpy_version,
            "liboqs_python_version": self.liboqs_python_version,
            "liboqs_version": self.liboqs_version,
            "cryptography_version": self.cryptography_version,
            "quantumsec_version": self.quantumsec_version,
            "os": self.os,
            "os_release": self.os_release,
            "os_version": self.os_version,
            "machine_architecture": self.machine_architecture,
            "cpu_identifier": self.cpu_identifier,
            "git_commit_sha": self.git_commit_sha,
            "git_worktree_dirty": self.git_worktree_dirty,
        }


def _distribution_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def _quantumsec_version() -> str | None:
    installed = _distribution_version("quantumsec")
    if installed is not None:
        return installed
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    try:
        project = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("project", {})
    except OSError, tomllib.TOMLDecodeError:
        return None
    version = project.get("version") if isinstance(project, dict) else None
    return version if isinstance(version, str) else None


def _git_state() -> tuple[str | None, bool | None]:
    repository = Path(__file__).resolve().parents[1]
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repository,
            check=False,
            capture_output=True,
            text=True,
            timeout=2,
        )
        status = subprocess.run(
            ["git", "status", "--porcelain=v1", "--untracked-files=normal"],
            cwd=repository,
            check=False,
            capture_output=True,
            text=True,
            timeout=2,
        )
    except OSError, subprocess.SubprocessError:
        return None, None
    sha = commit.stdout.strip()
    clean_sha = sha if commit.returncode == 0 and len(sha) == 40 else None
    dirty = bool(status.stdout.strip()) if status.returncode == 0 else None
    return clean_sha, dirty
