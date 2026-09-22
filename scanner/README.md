# Police scanner

One book per sweep, book0 -> book19, then wraps to book0.
State: pointer.json {"next": N}. Log: scan.log (one line per sweep).
Runs via the `rewrite-polish-scanner` daily cron; each run reviews bookN only,
fixes polish-level issues, pushes under the standing approval, and advances the pointer.
