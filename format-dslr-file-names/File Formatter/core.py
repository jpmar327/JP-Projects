"""
core.py — Film Formatter
Pure logic: file discovery, rename planning, copy execution, deletion.
No GUI dependencies. Safe to import anywhere.
"""

import os
import shutil


def get_file_types(folder_path: str) -> list[str]:
    """
    Return sorted list of unique file extensions found
    across all immediate subfolders of folder_path.
    """
    seen = set()
    for subfolder in os.listdir(folder_path):
        sub_path = os.path.join(folder_path, subfolder)
        if not os.path.isdir(sub_path):
            continue
        for fname in os.listdir(sub_path):
            if "." in fname:
                ext = fname.rsplit(".", 1)[-1].lower()
                if ext:
                    seen.add(ext)
    return sorted(seen)


def build_rename_plan(
    folder_path: str,
    subfolder: str,
    files_prefix: str,
    month: str,
    year: str,
) -> list[tuple[str, str]]:
    """
    Build an ordered list of (old_abs_path, new_abs_path) copy pairs.

    Naming convention:
        <output>/<ext>/<prefix>_<month>_<year>_<00001>.ext

    Grouping rule (matches original script):
        Files that share the same stem in the same source subfolder are
        considered the same shot in different formats (e.g. .jpg + .nef).
        They receive the same counter number. The counter increments only
        when a new stem is encountered.

    Counter is independent per file extension.
    Source subfolders are processed in os.listdir() order (filesystem order),
    matching the original script behaviour.
    """
    # Collect source dirs, skip output subfolder if it already exists
    source_dirs = [
        d for d in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, d)) and d != subfolder
    ]

    # Build per-extension entry list: [(source_dir, stem, filename), ...]
    ext_map: dict[str, list[tuple[str, str, str]]] = {}
    for dirfolder in source_dirs:
        dir_path = os.path.join(folder_path, dirfolder)
        for fname in os.listdir(dir_path):
            if "." not in fname:
                continue
            stem, ext = fname.rsplit(".", 1)
            ext_lower = ext.lower()
            ext_map.setdefault(ext_lower, []).append((dirfolder, stem, fname))

    plan: list[tuple[str, str]] = []

    for ext, entries in ext_map.items():
        count = 0
        dsc_tracker = ""  # "source_dir/stem" of last processed entry

        for dirfolder, stem, fname in entries:
            key = f"{dirfolder}/{stem}"
            if key != dsc_tracker:
                dsc_tracker = key
                count += 1

            file_count_str = str(count).zfill(5)
            old_abs = os.path.join(folder_path, dirfolder, fname)
            new_abs = os.path.join(
                folder_path, subfolder, ext,
                f"{files_prefix}_{month}_{year}_{file_count_str}.{ext}",
            )
            plan.append((old_abs, new_abs))

    return plan


def execute_plan(
    plan: list[tuple[str, str]],
    log_fn=None,
    progress_fn=None,
) -> list[str]:
    """
    Copy files according to plan.

    Args:
        plan:        List of (src_abs_path, dst_abs_path) pairs.
        log_fn:      Optional callable(msg: str) for progress messages.
        progress_fn: Optional callable(current: int, total: int).

    Returns:
        Sorted list of unique source subfolder absolute paths that were touched.
    """
    touched_dirs: set[str] = set()
    n = len(plan)

    for i, (src, dst) in enumerate(plan, 1):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        touched_dirs.add(os.path.dirname(src))
        if log_fn:
            log_fn(f"Copied → {os.path.basename(dst)}")
        if progress_fn:
            progress_fn(i, n)

    return sorted(touched_dirs)


def delete_source_folders(source_dirs: list[str], log_fn=None):
    """
    Delete each path in source_dirs as a full directory tree.

    Args:
        source_dirs: List of absolute directory paths to remove.
        log_fn:      Optional callable(msg: str) for status messages.
    """
    for d in source_dirs:
        shutil.rmtree(d)
        if log_fn:
            log_fn(f"Deleted  ← {os.path.basename(d)}/")
