import ast
from pathlib import Path


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


def test_qkd_and_pqc_remain_independent_lower_domains() -> None:
    root = Path(__file__).resolve().parents[2]
    assert not (_top_level_imports(root / "qkd") & {"pqc", "orchestration"})
    assert not (_top_level_imports(root / "pqc") & {"qkd", "orchestration"})
