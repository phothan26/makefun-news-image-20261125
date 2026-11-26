// "THE WORLD" — Wednesday 25 November 2026, six stories in one image.
//
// The finished front page lives in this repository as entry.png.b64: the
// PNG, base64-encoded so it travels as a single line of plain text. This
// program decodes it and writes the bytes to /output/entry.png. It draws
// nothing and fetches nothing: the grader runs with no network and no
// browser, so the only work here is a faithful copy — decode, check the
// bytes are a whole PNG under the gate's size cap, write them, then read
// the file back and prove the copy is byte for byte the same image.
//
// Run it outside the grader like this:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { chmodSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

function fail(message: string): never {
  process.stderr.write(`news-image-20261125: ${message}\n`);
  process.exit(1);
}

// The grader provides /output; creating it when it is missing is harmless.
// Its permissions are never touched — only the file this program writes.
mkdirSync(outDir, { recursive: true });

// entry.png.b64 holds the image as one long base64 line. Any whitespace is
// stripped so the file stays readable in an editor and in a diff.
const encoded = readFileSync(join(here, "entry.png.b64"), "utf8").replace(/\s+/g, "");
const image = Buffer.from(encoded, "base64");

// A PNG is whole only if it opens with its 8-byte signature and closes
// with the 12-byte IEND chunk, and stays under the gate's 1 MiB cap.
// Checking before writing means a corrupt source fails loudly here
// instead of handing the judge a broken file.
const SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const IEND = Buffer.from([
  0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82,
]);
if (image.length === 0 || image.length > 1048576) {
  fail(`decoded image is ${image.length} bytes, outside the 1 MiB gate`);
}
if (!image.subarray(0, 8).equals(SIGNATURE)) {
  fail("decoded bytes do not start with the PNG signature");
}
if (!image.subarray(image.length - 12).equals(IEND)) {
  fail("decoded bytes do not end with the PNG IEND chunk");
}

// The IHDR chunk sits right after the signature: bytes 12-15 spell IHDR,
// bytes 16-19 hold the width and 20-23 the height, all big-endian. The
// gate wants a 1024 by 1024 image, so a decoded PNG of any other size
// fails here instead of reaching the judge.
if (image.subarray(12, 16).toString("ascii") !== "IHDR") {
  fail("decoded bytes have no IHDR chunk after the PNG signature");
}
const width = image.readUInt32BE(16);
const height = image.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  fail(`decoded image is ${width}x${height}, expected 1024x1024`);
}

writeFileSync(target, image);

// The file the judge reads must be world-readable; the directory it sits
// in is the grader's own, so only the file we just created gets a chmod.
try {
  chmodSync(target, 0o644);
} catch {
  // A read-only filesystem that already exposes the file is fine.
}

const written = readFileSync(target);
if (!written.equals(image)) {
  fail("output file differs from the decoded image");
}

process.stdout.write(`news-image-20261125: wrote ${target} (${image.length} bytes)\n`);
