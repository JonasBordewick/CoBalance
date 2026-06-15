#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: unity_simulation_runner.py
Author: Jonas Bordewick
Date: 22.03.2026
Contact: jonas.bordewick@uni-a.de
"""
import datetime
import os.path
import plistlib
import subprocess
import threading
from typing import Optional

from app.domain.simulation import SimulationJob, SimulationRunResult


class UnitySimulationRunner:
    """
    Runs Unity in batch mode as a subprocess and blocks until it exits.

    A single Lock guards both _process and _cancel_requested so that cancel()
    can safely be called from the main thread while run() is blocking on the
    worker thread.
    """

    def __init__(self):
        self._process: Optional[subprocess.Popen[str]] = None
        self._cancel_requested = False
        self._lock = threading.Lock()

    @property
    def is_running(self) -> bool:
        with self._lock:
            return self._process is not None and self._process.poll() is None

    def run(self, job: SimulationJob) -> SimulationRunResult:
        """
        Launches Unity and blocks until the process exits.

        The entire Popen + communicate() block is held under the lock so that
        cancel() can safely read and terminate _process from the main thread
        without a race condition. The lock is released again in the finally
        block by setting _process back to None.
        """
        self._validate_job(job)

        started_at_dt = datetime.datetime.now()
        started_at = started_at_dt.isoformat(timespec="seconds")

        self._cancel_requested = False
        command = self._build_command(job)

        try:
            with self._lock:
                self._process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=job.project_path,
                )

                # communicate() blocks until the process exits and captures all output.
                stdout, stderr = self._process.communicate()
                exit_code = self._process.returncode if self._process.returncode is not None else -1

                finished_at_dt = datetime.datetime.now()
                finished_at = finished_at_dt.isoformat(timespec="seconds")

                # A cancelled run is also treated as failed even if Unity exits cleanly
                # (exit code 0), because the result data will be incomplete.
                success = (exit_code == 0) and not self._cancel_requested

                if not success:
                    self._write_fallback_error_log(job, stdout, stderr)

                return SimulationRunResult(
                    success,
                    exit_code,
                    started_at,
                    finished_at
                )
        except Exception:
            finished_at_dt = datetime.datetime.now()
            finished_at = finished_at_dt.isoformat(timespec="seconds")

            return SimulationRunResult(
                success=False,
                exit_code=-1,
                started_at=started_at,
                finished_at=finished_at,
            )
        finally:
            with self._lock:
                self._process = None

    def cancel(self) -> None:
        with self._lock:
            self._cancel_requested = True

            if self._process is None:
                return

            if self._process.poll() is not None:
                return

            try:
                self._process.terminate()
            except Exception as e:
                pass

    @staticmethod
    def _resolve_executable_path(path: str) -> str:
        """
        Resolves the path to the actual Unity executable.

        On macOS, the Unity Editor is an application bundle (a directory
        ending in ".app"), which os.path.isfile() does not recognize and
        which cannot be executed directly. The real binary lives inside
        Contents/MacOS, named after the bundle's CFBundleExecutable entry.
        """
        if os.path.isfile(path):
            return path

        if path.endswith(".app") and os.path.isdir(path):
            executable_name = "Unity"
            info_plist_path = os.path.join(path, "Contents", "Info.plist")
            try:
                with open(info_plist_path, "rb") as info_plist_file:
                    info_plist = plistlib.load(info_plist_file)
                executable_name = info_plist.get("CFBundleExecutable", executable_name)
            except Exception:
                pass

            bundled_executable_path = os.path.join(path, "Contents", "MacOS", executable_name)
            if os.path.isfile(bundled_executable_path):
                return bundled_executable_path

        return path

    @staticmethod
    def _validate_job(job: SimulationJob) -> None:
        if not job.unity_application_path:
            raise ValueError("unity_application_path is required.")
        if not os.path.isfile(UnitySimulationRunner._resolve_executable_path(job.unity_application_path)):
            raise FileNotFoundError(f"Unity application not found at {job.unity_application_path}")

        if not job.project_path:
            raise ValueError("project_path is required.")
        if not os.path.isdir(job.project_path):
            raise FileNotFoundError(f"Unity project path not found: {job.project_path}")

        if not job.job_file_path:
            raise ValueError("job_file_path is required.")
        if not os.path.isfile(job.job_file_path):
            raise FileNotFoundError(f"Unity job file not found at {job.job_file_path}")

    @staticmethod
    def _build_command(job: SimulationJob) -> list[str]:
        base = [
            UnitySimulationRunner._resolve_executable_path(job.unity_application_path),
            "-projectPath", job.project_path,
            "-batchmode",
            "-nographics",
            "-executeMethod", "CoBalance.Editor.SimulationBatchEntry.Run",
            "-jobConfig", job.job_file_path,
            # "-logFile", "C:\\Users\\Jonas Bordewick\\Documents\\Masterthesis\\CoBalance\\app\\dist\\log.txt"
        ]
        if job.create_logs:
            return base
        return base + ["-ignoreLog"]
    @staticmethod
    def _write_fallback_error_log(job: SimulationJob, stdout: str, stderr: str) -> None:
        try:
            output_dir = os.path.dirname(job.job_file_path) or job.project_path
            error_log_path = os.path.join(
                output_dir,
                f"unity_runner_error.log",
            )

            with open(error_log_path, "w", encoding="utf-8") as file:
                file.write("=== STDOUT ===\n")
                file.write(stdout or "")
                file.write("\n\n=== STDERR ===\n")
                file.write(stderr or "")
        except Exception:
            pass
