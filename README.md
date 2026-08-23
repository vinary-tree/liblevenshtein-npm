# `liblevenshtein` npm compatibility package

This repository owns the unscoped [`liblevenshtein`](https://www.npmjs.com/package/liblevenshtein)
package beginning with `4.0.0-rc.1`. It is a deliberately thin compatibility
name for the Rust-backed `@vinary-tree/liblevenshtein` facade and therefore
shares the same native Node, browser WebAssembly, and WASI implementations.

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

Run `npm test` and inspect `npm pack --dry-run`. A release tag must equal
`v4.0.0-rc.1`; publication uses npm trusted publishing and an explicit
`--tag next`. Do not run `npm dist-tag add liblevenshtein@4.0.0-rc.1 latest`
during the RC campaign.
