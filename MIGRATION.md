# Migrating `liblevenshtein` from version 2 to version 4

Version 4 changes both the implementation and the public object model. The
unscoped package name remains available, but it delegates to the Rust-backed
`@vinary-tree/liblevenshtein` facade rather than emulating the version 2 API.

Install the candidate explicitly:

```bash
npm install liblevenshtein@next @vinary-tree/libdictenstein@next
```

Dictionary construction now belongs to libdictenstein. Matching consumes its
retained dictionary resource:

```js
import { dynamicDawg } from "@vinary-tree/libdictenstein";
import { transducer } from "liblevenshtein";

using dictionary = dynamicDawg(["cat", "cot", "cut"]);
using automaton = transducer(dictionary, "standard");
using cursor = automaton.query("cat", 1);

for (const match of cursor) {
  console.log(match.term, match.distance);
}
```

On JavaScript engines without explicit resource management, close the resources
in `finally` blocks in reverse construction order. Garbage-collection
finalizers are leak containment, not the primary lifetime mechanism.

| Version 2 concern | Version 4 replacement |
|---|---|
| Dictionary and matching API shipped together | Construct dictionaries with `@vinary-tree/libdictenstein`; pass their resource to `liblevenshtein` |
| Package-selected JavaScript implementation | One exact `@vinary-tree/vinary-tree` runtime supplies native, browser-WASM, and WASI exports |
| Whole-result convenience as the normal path | Iterate a query cursor or reduce bounded batches |
| Implicit numeric identifiers | Use `bigint` for unsigned 64-bit identifiers |
| GC as the visible resource boundary | Use `using` or explicit `close()` |

The unscoped and scoped liblevenshtein packages expose the same entry points:
`.`, `./typescript`, `./clojurescript`, `./wasm`, and `./wasi`. The unscoped
package contains no native binary, so switching the import spelling does not
create a second runtime identity.

During the RC, `liblevenshtein@latest` remains version `2.0.4`. Pin
`liblevenshtein@4.0.0-rc.3` or use the `next` dist-tag when evaluating version
4.
