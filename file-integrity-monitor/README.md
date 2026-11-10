# File Integrity Monitor

This tool records SHA-256 hashes for files in a directory. Run it again later to see which files were added, changed, or removed.

It is a small file-integrity-monitoring exercise, not an endpoint security product. It does not stop changes or identify who made them.

## Create a baseline

Keep the baseline outside the folder being monitored:

```bash
python file_integrity_monitor.py baseline ./sample-folder --manifest ./baseline.json
```

## Check for changes

```bash
python file_integrity_monitor.py verify ./sample-folder --manifest ./baseline.json
```

The verify command exits with code `0` when no changes are found, `1` when files differ, and `2` when it cannot complete the check.

## Notes

- Uses SHA-256 and reads files in chunks.
- Does not follow symbolic links.
- Store the baseline somewhere with appropriate access controls. If an attacker can replace both the files and the baseline, the comparison can be fooled.
- The tool reports file changes; it does not preserve file contents or restore deleted files.
