import ast
import json
from dataclasses import replace
from pathlib import Path

import pytest

from experiments import ExperimentConfig, ExperimentKind
from experiments.export import config_from_json, load_config_json
from orchestration import SessionConfig, SessionProfile
from qkd.channel import QKDChannelStageSpec, QKDChannelStageType


def test_experiment_kind_has_the_six_v1_labels() -> None:
    assert tuple(kind.value for kind in ExperimentKind) == ("E1", "E2", "E3", "E4", "E5", "D1")


def test_config_round_trip_preserves_normalized_meaning(e3_config) -> None:
    public = e3_config.to_public_dict()
    restored = ExperimentConfig.from_public_dict(json.loads(json.dumps(public)))
    assert restored == e3_config
    assert restored.to_public_dict() == public
    assert restored.qkd_stages[0].intercept_fraction == 0.5


def test_example_configs_load_without_runtime_secrets() -> None:
    qkd = load_config_json("examples/experiments/qkd_eve_example.json")
    pqc = load_config_json("examples/experiments/pqc_base_example.json")
    assert qkd.experiment_kind is ExperimentKind.E3_INTERCEPT_RESEND
    assert pqc.profile is SessionProfile.PQC_BASE
    serialized = json.dumps([qkd.to_public_dict(), pqc.to_public_dict()]).lower()
    assert "private_key" not in serialized
    assert "session_key" not in serialized
    assert "psk" not in serialized


def test_config_rejects_obvious_ambiguities(qkd_config) -> None:
    with pytest.raises(ValueError, match="replicate_index"):
        replace(qkd_config, replicate_index=-1)
    with pytest.raises(ValueError, match="require a seed"):
        replace(qkd_config, seed=None)
    with pytest.raises(ValueError, match="PQC-only"):
        ExperimentConfig(
            ExperimentKind.E1_PQC_COST,
            "invalid-pqc-stage",
            0,
            SessionConfig(SessionProfile.PQC_BASE),
            qkd_stages=(QKDChannelStageSpec(QKDChannelStageType.IDENTITY),),
        )
    with pytest.raises(ValueError, match="does not accept"):
        QKDChannelStageSpec(QKDChannelStageType.IDENTITY, p=0.1)
    with pytest.raises(ValueError, match="Pauli"):
        QKDChannelStageSpec(QKDChannelStageType.PAULI, px=0.5, py=0.5, pz=0.1)


def test_json_loader_rejects_duplicate_and_unknown_fields(qkd_config) -> None:
    text = json.dumps(qkd_config.to_public_dict())
    with pytest.raises(ValueError, match="Duplicate JSON field"):
        config_from_json('{"version": 1, "version": 1}')
    data = json.loads(text)
    data["secret_blob"] = "forbidden-by-schema"
    with pytest.raises(ValueError, match="Unknown experiment config fields"):
        ExperimentConfig.from_public_dict(data)


def _top_level_imports(root: Path) -> set[str]:
    imported: set[str] = set()
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
    return imported


def test_experiment_dependency_direction_is_not_inverted() -> None:
    root = Path(__file__).resolve().parents[2]
    experiment_imports = _top_level_imports(root / "experiments")
    assert "orchestration" in experiment_imports
    assert "ui" not in experiment_imports
    for lower_layer in ("orchestration", "qkd", "pqc", "data_protection"):
        assert "experiments" not in _top_level_imports(root / lower_layer)
