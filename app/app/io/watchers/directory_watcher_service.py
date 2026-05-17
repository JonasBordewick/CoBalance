#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: directory_watcher_service.py
Author: Jonas Bordewick
Date: 22.03.2026
Contact: jonas.bordewick@uni-a.de
"""
from PyQt6.QtCore import QFileSystemWatcher, pyqtSignal, QObject

from app.enums import WatchType


class DirectoryWatcherService(QObject):
    """Wraps QFileSystemWatcher to provide a keyed, multi-path watch service.

    Each path is registered under a string key so consumers can identify which
    of their watched paths triggered a change. Both signals carry an is_initial
    flag that is True on first registration and False on subsequent filesystem events.

    Signals:
        watched_file_changed(key, path, is_initial)
        watched_directory_changed(key, path, is_initial)
    """

    watched_file_changed = pyqtSignal(str, str, bool)
    watched_directory_changed = pyqtSignal(str, str, bool)

    def __init__(self):
        super().__init__()

        self._watched_entries: dict[str, tuple[str, WatchType]] = dict() # [key, (path, watch_type)]

        self._file_watcher = QFileSystemWatcher()
        self._file_watcher.fileChanged.connect(self._on_file_changed)
        self._file_watcher.directoryChanged.connect(self._on_directory_changed)

    # Public API

    def watch_directory(self, directory_key: str, directory_path: str):
        self._watch(directory_key, directory_path, WatchType.DIRECTORY)

    def watch_file(self, file_key: str, file_path: str):
        self._watch(file_key, file_path, WatchType.FILE)

    def unwatch(self, entry_key: str):
        if entry_key not in self._watched_entries:
            return
        path, _ = self._watched_entries.get(entry_key)
        self._file_watcher.removePath(path)
        self._watched_entries.pop(entry_key)

    # Private Methods

    def _watch(self, entry_key: str, entry_path: str, watch_type: WatchType):
        """Registers a path under a key, replacing any previously watched path for that key."""
        if not entry_path.strip():
            print(f"{entry_key} has no path")
            return
        if entry_key in self._watched_entries:
            old_entry_path, _ = self._watched_entries.get(entry_key, ("", WatchType.FILE))
            self._file_watcher.removePath(old_entry_path)
        self._watched_entries[entry_key] = (entry_path, watch_type)
        self._file_watcher.addPath(entry_path)
        self._notify_changes(entry_key, entry_path, watch_type)

    def _notify_changes(self, entry_key: str, entry_path: str = None, watch_type: WatchType = None):
        if watch_type == WatchType.DIRECTORY:
            self.watched_directory_changed.emit(entry_key, entry_path, True)
        elif watch_type == WatchType.FILE:
            self.watched_file_changed.emit(entry_key, entry_path, True)

    def _on_file_changed(self, path):
        self._on_changes(path, WatchType.FILE)

    def _on_directory_changed(self, path):
        self._on_changes(path, WatchType.DIRECTORY)

    def _on_changes(self, path: str, changed_type: WatchType):
        for entry_key, (entry_path, watch_type) in self._watched_entries.items():
            if entry_path == path and watch_type == changed_type:
                if watch_type == WatchType.DIRECTORY:
                    self.watched_directory_changed.emit(entry_key, entry_path, False)
                elif watch_type == WatchType.FILE:
                    self.watched_file_changed.emit(entry_key, entry_path, False)
                break
