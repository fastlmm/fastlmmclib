# fastlmmclib

C extensions for FaST-LMM Python Project

Requires Python 3.11 or later. Python 3.15 qualification is in progress.

## 1.0.0 (unreleased)

- Prepare Python 3.11 through 3.15 native wheels with Cython 3.3.1 and
  cibuildwheel 4.3.5; cross-platform qualification is required before release.
- Regenerate the C++ wrapper from the maintained Cython source.
- Preserve the QFC algorithm and add checks against an analytic chi-square
  survival function, including installed wheel and source-distribution tests.

Regenerate the committed wrapper with its full module name:

```console
uvx --python 3.14 --from Cython==3.3.1 --with numpy==2.5.4 cython \
  --cplus -3 --module-name fastlmmclib.quadform.qfc_src.wrap_qfc \
  fastlmmclib/quadform/qfc_src/wrap_qfc.pyx
```
