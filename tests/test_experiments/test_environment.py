from experiments import ExperimentEnvironment


def test_environment_snapshot_contains_reproducibility_context() -> None:
    environment = ExperimentEnvironment.capture()
    public = environment.to_public_dict()
    assert public["python_version"]
    assert public["python_implementation"]
    assert public["numpy_version"]
    assert public["cryptography_version"]
    assert public["quantumsec_version"]
    assert public["os"]
    assert public["machine_architecture"]
    assert public["git_commit_sha"] is None or len(str(public["git_commit_sha"])) == 40
    assert public["git_worktree_dirty"] is None or isinstance(public["git_worktree_dirty"], bool)
    assert all("key" not in name.lower() for name in public)
