import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const packageJson = JSON.parse(await readFile(new URL("../package.json", import.meta.url)));
const versionModel = JSON.parse(await readFile(new URL("../release/version.json", import.meta.url)));

test("the unscoped RC delegates to one exact scoped facade", () => {
  assert.equal(packageJson.name, "liblevenshtein");
  assert.deepEqual(packageJson.dependencies, {
    "@vinary-tree/liblevenshtein": "4.0.0-rc.6",
  });
  assert.equal(packageJson.publishConfig.tag, "next");
});

test("the legacy latest dist-tag is explicitly protected", () => {
  assert.deepEqual(versionModel.legacyLatest, {
    version: "2.0.4",
    mustRemainUnchangedDuringRc: true,
  });
});

test("every export is a thin delegation surface", async () => {
  for (const path of [
    "index.mjs", "index.cjs", "index.d.ts",
    "typescript.mjs", "typescript.cjs", "typescript.d.ts",
    "clojurescript.mjs", "clojurescript.cjs", "clojurescript.d.ts",
    "wasm.mjs", "wasm.d.ts", "wasi.mjs", "wasi.d.ts",
  ]) {
    const source = await readFile(new URL(`../${path}`, import.meta.url), "utf8");
    assert.match(source, /@vinary-tree\/liblevenshtein/);
  }
});
