# Releasing fastlmmclib

The maintainer chooses the version and explicitly approves publication. A
release must be built from a clean commit on `main`, and its `vX.Y.Z` tag must
point to that exact commit.

## Release order

Publish and verify `fastlmmclib` before final qualification of a FaST-LMM
release that depends on it. Final acceptance must install the published
artifact from PyPI rather than a sibling checkout or an unpublished wheel.

## One-time repository setup

- Configure a PyPI Trusted Publisher for repository
  `fastlmm/fastlmmclib`, workflow `publish.yml`, and environment `pypi`.
- Create a protected GitHub environment named `pypi`, require maintainer
  approval, and restrict deployment to version tags when GitHub's environment
  settings permit it.
- Do not store a PyPI password or API token in GitHub.

The Build workflow produces and tests the native wheels and source
distribution. After a successful version-tag Build, the Publish workflow
downloads those exact artifacts, verifies their tag, commit, version, and file
set, and publishes them with PyPI Trusted Publishing. It does not rebuild the
distributions.

## Prepare the release

1. Start from a clean release branch based on current `main`.
2. Review open issues, pull requests, and dependency advisories that could
   affect the release.
3. Set the version in `setup.py` and update user-facing release notes.
4. Confirm that supported Python versions and dependency bounds match the
   wheel matrix and environments actually tested.
5. Run the complete tests and lint checks locally where practical.
6. Build and inspect the source distribution. Confirm that it contains the C,
   Cython, header, license, and metadata files required to build a wheel.
7. Install and test built artifacts outside the source checkout, without the
   repository on `PYTHONPATH`.
8. Merge the reviewed change and require a successful Build run on the exact
   `main` commit before tagging it.

## Publish

1. Confirm that the version is absent from PyPI and that the tag is unused.
2. Create and push an annotated tag on the qualified `main` commit:

   ```console
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   git push origin vX.Y.Z
   ```

3. Verify that the tag's Build workflow succeeds for every wheel platform and
   for the source-distribution test.
4. Review and approve the protected `pypi` environment in the automatically
   triggered Publish workflow.
5. Confirm that PyPI received the source distribution and the complete wheel
   set, with attestations.
6. Create a matching GitHub release and attach or link the release notes.

## Publish an already-built tag

The Publish workflow can recover a successful tagged Build whose automatic
publish step was unavailable. Run it manually from GitHub Actions and provide
the tagged Build run ID and its existing `vX.Y.Z` tag. The workflow rejects a
failed run, a branch build, a moved or mismatched tag, and unexpected files.

Never move an existing release tag to make this recovery path work.

## Verify the published release

- Install `fastlmmclib==X.Y.Z` from PyPI in clean environments on the oldest
  and newest supported Python versions.
- Run representative native-extension tests without a source checkout on
  `PYTHONPATH`.
- Inspect PyPI's file list for every intended operating system, architecture,
  and Python version.
- Run the relevant InstallTest scenarios before releasing FaST-LMM.

## Failed releases

Do not replace files under an existing PyPI version or move its tag. If a
published release is unusable, yank it with a concise reason and publish a new
version. Preserve the failed release's tag and CI evidence for traceability.
