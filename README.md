# `liblevenshtein` npm compatibility package

This repository owns the unscoped [`liblevenshtein`](https://www.npmjs.com/package/liblevenshtein)
package for version 4 release candidates. It is a deliberately thin
compatibility name for the Rust-backed `@vinary-tree/liblevenshtein` facade and
therefore shares the same native Node, browser WebAssembly, and WASI
implementations.

```sh
npm install liblevenshtein@next
```

```js
import { transducer } from "liblevenshtein";
```

Version 4 is a new major API. It does not claim source compatibility with the
legacy JavaScript package. Existing users remain on `liblevenshtein@latest`
version `2.0.4` during the release-candidate period; the Rust-backed candidate
is published only under `next` until the migration guide and release gates are
complete.

See [MIGRATION.md](MIGRATION.md) for the version-2-to-version-4 package and
resource-lifetime changes.

The implementation is one level of delegation:

`liblevenshtein` → `@vinary-tree/liblevenshtein` → `@vinary-tree/vinary-tree`.

The unscoped package contains no native binary and no second runtime identity.
Its ESM, CommonJS, TypeScript, ClojureScript, WASM, and WASI subpaths re-export
the exact scoped package version recorded in `release/version.json`.

## Release safety

Run `npm test` and inspect `npm pack --dry-run`. The release workflow accepts
only the exact immutable source tag recorded in `release/version.json`; that
tag must be the canonical `v4.0.0-rc.5` tag or a positive numbered append-only
correction. Publication uses npm trusted publishing and an explicit
`--tag next`. Do not run `npm dist-tag add liblevenshtein@4.0.0-rc.5 latest`
during the RC campaign.

Updating a branch does not create or authorize a source tag. The
`github-release` environment requires operator review and a `v*` tag policy,
while npm remains behind its trusted-publisher environment. If a tagged source
must be corrected, create a new `v4.0.0-rc.5-release.N` ref and update
`sourceTag`; never move an existing tag.

Tag creation establishes only the immutable source ref. Dispatch
`registry=validate-only` to pack the compatibility facade and attach the
tarball plus SHA-256 manifest to a GitHub prerelease without mutating npm.
After `@vinary-tree/liblevenshtein@4.0.0-rc.5` resolves and passes an
installed-package smoke test, publish this final dependency-graph leaf with an
exact-tag dispatch:

```bash
gh workflow run release.yml \
  --repo vinary-tree/liblevenshtein-npm \
  --ref v4.0.0-rc.5 \
  -f registry=npm
```

Use `registry=validate-only` to rerun the artifact and GitHub-prerelease lane
without authorizing npm. Branch dispatches fail closed. After publication,
verify `next = 4.0.0-rc.5` and `latest = 2.0.4`; unlike the six new scoped
packages, this legacy coordinate must not move `latest` during the RC.
