from __future__ import annotations

import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Callable

from .store import WorkspaceStore


JobFunction = Callable[[Callable[[int, int, str, str], None]], dict[str, Any]]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class JobManager:
    def __init__(self, store: WorkspaceStore, worker_count: int = 2):
        self.store = store
        self.executor = ThreadPoolExecutor(max_workers=max(1, worker_count), thread_name_prefix="cmbx-web")
        self._futures: dict[str, Any] = {}
        self._lock = Lock()

    def submit(
        self,
        *,
        workspace_id: str,
        owner: str,
        task_type: str,
        input_payload: dict[str, Any],
        function: JobFunction,
    ) -> dict[str, Any]:
        job_id = uuid.uuid4().hex
        job = self.store.create_job(
            {
                "id": job_id,
                "workspace_id": workspace_id,
                "owner": owner,
                "task_type": task_type,
                "input": input_payload,
                "message": "Waiting for an available worker",
            }
        )
        future = self.executor.submit(self._run, job_id, function)
        with self._lock:
            self._futures[job_id] = future
        future.add_done_callback(lambda _future: self._forget(job_id))
        return job

    def _run(self, job_id: str, function: JobFunction) -> None:
        self.store.update_job(
            job_id,
            status="preparing",
            stage="preparing",
            started_at=utc_now(),
            message="Preparing task",
        )

        def progress(current: int, total: int, stage: str, message: str) -> None:
            self.store.update_job(
                job_id,
                status="running" if stage not in {"validating", "completed"} else stage,
                progress_current=max(0, current),
                progress_total=max(1, total),
                stage=stage,
                message=message,
            )

        try:
            result = function(progress)
            self.store.update_job(
                job_id,
                status="completed",
                stage="completed",
                progress_current=1,
                progress_total=1,
                message="Task completed",
                result_json=result,
                finished_at=utc_now(),
            )
        except Exception as exc:
            self.store.update_job(
                job_id,
                status="failed",
                stage="failed",
                message=str(exc),
                error="".join(traceback.format_exception_only(type(exc), exc)).strip(),
                finished_at=utc_now(),
            )

    def _forget(self, job_id: str) -> None:
        with self._lock:
            self._futures.pop(job_id, None)

    def active_count(self) -> int:
        with self._lock:
            return len(self._futures)

    def shutdown(self) -> None:
        self.executor.shutdown(wait=False, cancel_futures=False)
