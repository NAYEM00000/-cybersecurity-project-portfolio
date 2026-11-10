# Review notes

This is a learning repository. The following checks were added as the project set grew:

- Input validation for password lengths, CSV thresholds, ports, and URLs.
- Exact cookie-attribute parsing rather than substring matching.
- Deterministic alert ordering in the CSV analyzers.
- SHA-256 file comparison with symlink traversal disabled.
- TLS certificate inspection through Python's default verified SSL context.
- Unit tests for core parsing, validation, and comparison behavior.

The checks do not prove that a tool is production-ready. They cover selected expected inputs and edge cases. The URL score and password score are deliberately described as heuristics, and the network tools should only be used with authorized targets or data.
