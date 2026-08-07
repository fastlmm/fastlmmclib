# Coding Notes for Agents

This file contains repository-wide guidance for `fastlmmclib`, a Python package
with a compiled Cython/C++ extension used by FaST-LMM. Preserve numerical
correctness, binary-package reliability, and downstream compatibility unless a
task explicitly changes those goals.

## General Policies

- When work is interrupted or reaches a stopping point, report the current
  status, what remains, and the recommended next step. If the next step is
  within the current task and safe to perform, perform it instead of merely
  recommending it.
- Inspect the Python wrapper, Cython source, C++ implementation, tests,
  packaging configuration, and CI before introducing a new pattern. Keep
  changes focused and avoid unrelated rewrites.
- Do not silently skip required Python versions, operating systems,
  architectures, compilers, tests, or wheel checks. If a required environment
  or tool is unavailable, fail clearly and report what is missing.
- Avoid silent clamping, coercion, truncation, precision loss, or fallback
  behavior. Validate inputs and fail clearly unless the public API explicitly
  documents another behavior.

## Cross-Repository Release Coordination

`fastlmmclib` is released independently and is consumed by FaST-LMM. For
coordinated compatibility releases, publish and validate its native artifacts
before qualifying FaST-LMM, and perform final acceptance against published
artifacts rather than an unpublished sibling checkout.

## Numerical and Native-Code Correctness

- Treat changes to the quadratic-form algorithm, convergence behavior,
  tolerances, iteration limits, floating-point types, memory layout, and native
  compiler flags as behavior changes, not mechanical refactors.
- Do not update expected numerical output merely to make a test pass. First
  confirm that the result is correct and does not hide a precision, stability,
  or platform regression.
- When exact equality is inappropriate, use an explicit, justified tolerance.
  Include boundary, degenerate, and representative FaST-LMM inputs where
  practical.
- Check ownership, lifetime, bounds, shape, dtype, and contiguity assumptions at
  the Python/Cython/C++ boundary. Do not trade safety for speed without a
  documented justification and targeted tests.
- Avoid introducing undefined behavior or unchecked memory access. Call out and
  justify any unavoidable low-level operation that cannot be made evidently
  safe.

## Python, Cython, and C++ Sources

- Treat `fastlmmclib/quadform/qfc_src/wrap_qfc.pyx` as the source of truth for
  the Cython wrapper. Its generated `wrap_qfc.cpp` must stay synchronized when
  retained in the source distribution.
- Do not hand-edit generated Cython C++ output as the sole fix. Change the `.pyx`
  source, regenerate with the reviewed Cython version, and inspect the generated
  diff.
- Treat `QFC.cpp` and `QFC.h` as maintained native sources, not generated files.
  Preserve their algorithmic behavior and platform portability.
- Keep platform-specific macros and compiler options narrow. Test Windows,
  Linux, Intel macOS, and Apple Silicon behavior affected by native changes.
- Keep implementation details private; do not expose native helpers in the
  Python API solely for internal convenience.

## Error Handling

- Preserve useful diagnostics across the C++/Cython/Python boundary. Translate
  native failures into specific Python exceptions without discarding context.
- In Python, use exception chaining (`raise ... from error`) when adding
  context. Catch only exceptions that can be handled meaningfully.
- Do not return sentinel values, swallow compiler or linker failures, or use a
  broad `except` to make a failing path appear successful.
- Do not suppress warnings solely to quiet tests or CI. Fix the cause or
  document a narrow, justified suppression.

## Dependencies and Packaging

- Treat NumPy, Cython, setuptools, compiler, and `cibuildwheel` upgrades as
  behavior and ABI migrations, not just build fixes. Review changed APIs and
  defaults, then test the resulting extension.
- Keep build requirements and runtime requirements explicit with honest lower
  bounds. Use Python-version markers when newer interpreters require newer
  dependencies without unnecessarily raising requirements elsewhere.
- Keep `pyproject.toml`, `setup.py`, wheel configuration, package metadata, and
  supported-Python classifiers consistent.
- Build wheels for every supported Python/platform/architecture combination.
  Do not claim support for a target until its wheel installs and its tests pass
  in a clean environment.
- Test the installed wheel with the repository removed from `PYTHONPATH`. A
  passing test against an in-place extension or source checkout is not
  sufficient evidence that the wheel is correct.
- Build and inspect the source distribution when release behavior changes.
  Verify that it contains the required Cython/generated and native sources to
  build without relying on untracked local files.

## Tests and Validation

- Add or update tests for every behavior change and regression fix. A regression
  test should fail for the original defect and pass for the corrected behavior.
- Run the narrowest relevant tests while iterating, then run the complete pytest
  suite in `tests/test.py` against a built extension before handing work back.
- For native or packaging changes, also build wheels through the repository's
  `cibuildwheel` workflow or an equivalent local target and test the actual
  artifacts on the affected platforms.
- Validate supported boundary Python versions, including Python 3.10 and 3.14
  during the current modernization, rather than only the local interpreter.
- Do not disable, deselect, or weaken tests, doctests, lint rules, or CI jobs
  merely to obtain a passing result. Any exception must be narrow, documented,
  and reported.

## API, Comments, and Documentation

- Treat changes to public signatures, accepted input shapes or dtypes, defaults,
  return values, import paths, and exceptions as compatibility-sensitive.
- Prefer one clear canonical API path. Keep compatibility aliases only when
  downstream users require them, and document the canonical path.
- Preserve useful TODOs, algorithm notes, attribution, diagnostic code, and
  debugging comparisons while their underlying issue remains unresolved.
- Keep the README and package metadata synchronized with supported Python
  versions, platforms, installation behavior, and release requirements.
- Use American English. In Markdown, place blank lines around headings, lists,
  and fenced code blocks, and keep list markers consistent.

## Development and Release Safety

- Use project-local environments and the repository's documented toolchain. Do
  not silently install system-wide packages or alter unrelated global compiler
  or Python configuration.
- Do not publish a real release to PyPI or another package index. Agents may
  prepare version changes, release notes, artifacts, and commands, but a person
  must perform or explicitly authorize publication.
- Before handing work back, summarize validation performed, anything not run,
  and any numerical, ABI, packaging, platform, or release risk that remains.
