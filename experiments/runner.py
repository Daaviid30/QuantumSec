"""Thin observer around the common session runner."""

from __future__ import annotations

import random
from collections.abc import Callable, Iterable
from uuid import uuid4

from experiments.config import ExperimentConfig, ExperimentKind
from experiments.environment import ExperimentEnvironment
from experiments.record import BatchProvenance, ExperimentRecord
from experiments.runtime import ExperimentRuntimeFactory
from orchestration.runner import run_session


class ExperimentRunner:
    """Execute one configuration and retain only copied public evidence."""

    __slots__ = ("runtime_factory",)

    def __init__(self, runtime_factory: ExperimentRuntimeFactory) -> None:
        if not isinstance(runtime_factory, ExperimentRuntimeFactory):
            raise TypeError("runtime_factory must be an ExperimentRuntimeFactory.")
        self.runtime_factory = runtime_factory

    def run(
        self,
        config: ExperimentConfig,
        *,
        batch: BatchProvenance | None = None,
        execution_order_index: int | None = None,
    ) -> ExperimentRecord:
        if not isinstance(config, ExperimentConfig):
            raise TypeError("config must be an ExperimentConfig.")
        if config.experiment_kind is ExperimentKind.D1_PROTECTED_SESSION:
            raise ValueError(
                "D1_PROTECTED_SESSION requires the specialized data-plane runner to transfer "
                "K_SESSION before session closure."
            )
        environment = ExperimentEnvironment.capture()
        runtime = self.runtime_factory.build(config)
        session_result = run_session(config.session_config, runtime.context)
        try:
            return ExperimentRecord.from_session_result(
                config=config,
                environment=environment,
                provisioning=runtime.provisioning,
                session_result=session_result,
                batch=batch,
                execution_order_index=execution_order_index,
            )
        finally:
            session_result.close()


def run_batch(
    configs: Iterable[ExperimentConfig],
    runner: ExperimentRunner | None = None,
    *,
    shuffle: bool = False,
    order_seed: int | None = None,
    warmup_runs: int = 0,
    warmup_configs: Iterable[ExperimentConfig] = (),
    progress: Callable[[int, int, ExperimentRecord], None] | None = None,
) -> tuple[ExperimentRecord, ...]:
    """Run ordered configurations sequentially, optionally shuffling reproducibly.

    Warm-up executions are explicitly requested, executed before measurements,
    and discarded. ``order_seed`` controls only ordering, never BB84 randomness.
    """

    clean_configs = tuple(configs)
    if not clean_configs:
        raise ValueError("configs must contain at least one ExperimentConfig.")
    if not all(isinstance(config, ExperimentConfig) for config in clean_configs):
        raise TypeError("configs must contain only ExperimentConfig values.")
    if not isinstance(shuffle, bool):
        raise TypeError("shuffle must be a bool.")
    if shuffle:
        if isinstance(order_seed, bool) or not isinstance(order_seed, int) or order_seed < 0:
            raise ValueError("shuffle=True requires a non-negative integer order_seed.")
    elif order_seed is not None:
        raise ValueError("order_seed is only meaningful when shuffle=True.")
    if isinstance(warmup_runs, bool) or not isinstance(warmup_runs, int) or warmup_runs < 0:
        raise ValueError("warmup_runs must be a non-negative integer.")
    clean_warmups = tuple(warmup_configs)
    if not all(isinstance(config, ExperimentConfig) for config in clean_warmups):
        raise TypeError("warmup_configs must contain only ExperimentConfig values.")
    if progress is not None and not callable(progress):
        raise TypeError("progress must be callable or None.")

    active_runner = runner or ExperimentRunner(ExperimentRuntimeFactory())
    ordered = list(clean_configs)
    if shuffle:
        random.Random(order_seed).shuffle(ordered)
    for config in clean_warmups:
        active_runner.run(config)
    for index in range(warmup_runs):
        active_runner.run(ordered[index % len(ordered)])
    batch = BatchProvenance(
        batch_run_id=str(uuid4()),
        shuffle=shuffle,
        order_seed=order_seed,
        warmup_runs=len(clean_warmups) + warmup_runs,
    )
    records: list[ExperimentRecord] = []
    for index, config in enumerate(ordered):
        record = active_runner.run(config, batch=batch, execution_order_index=index)
        records.append(record)
        if progress is not None:
            progress(index + 1, len(ordered), record)
    return tuple(records)
