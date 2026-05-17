#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: simulation_worker.py
Author: Jonas Bordewick
Date: 22.03.2026
Contact: jonas.bordewick@uni-a.de
"""
from typing import Optional

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from app.domain.simulation import SimulationJob
from app.io.process import UnitySimulationRunner


class SimulationWorker(QObject):
    """Qt worker that runs a single simulation job on a background thread.

    Designed to be moved onto a QThread via moveToThread(). Emits finished or
    failed when done so the thread can be torn down cleanly.
    """

    progress_changed = pyqtSignal(int, int)
    job_finished = pyqtSignal(int, object)
    finished = pyqtSignal()
    failed = pyqtSignal(str)

    def __init__(self, job: SimulationJob, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._job = job
        self._cancel_requested = False
        self._runner =UnitySimulationRunner()

    @pyqtSlot()
    def run(self) -> None:
        """Executes the simulation job and emits finished or failed."""
        if self._cancel_requested:
            self.finished.emit()
            return

        self.progress_changed.emit(0, 0)

        try:
            result = self._runner.run(self._job)
        except Exception as e:
            self.failed.emit(f"Simulation run failed. {e}")
            return

        self.job_finished.emit(0, result)

        if not result.success and not self._cancel_requested:
            self.failed.emit(f"Simulation run {0}/{0} finished with exit code {result.exit_code}")
            return
        self.finished.emit()

    @pyqtSlot()
    def cancel(self) -> None:
        """Requests cancellation of the running simulation. Safe to call from any thread."""
        self._cancel_requested = True
        self._runner.cancel()