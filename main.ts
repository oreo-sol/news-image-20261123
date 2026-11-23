// news-image-20261123: copies the pre-rendered entry.png to the output dir.
// The image is drawn by dev/draw.py (seeded, deterministic) and pinned here
// by its sha256, so both grader runs write the same bytes.
import { createHash } from "node:crypto";
import { copyFileSync, existsSync, readFileSync, statSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const ENTRY = "entry.png";
const ENTRY_SHA256 = "644ecc526a7fff6d44dd6488a5f0af3678fcac8b3411f71cd76120dd2cc22694";
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function fail(msg: string): never {
  throw new Error(msg);
}

if (!existsSync(ENTRY)) fail("entry.png not found");
const buf = readFileSync(ENTRY);
if (buf.length > 1048576) fail(`entry.png too large: ${buf.length} bytes`);
if (!buf.subarray(0, 8).equals(PNG_SIG)) fail("entry.png is not a PNG");
// A whole PNG ends with its IEND chunk (12 bytes: length 0, "IEND", CRC).
const IEND = Buffer.from([0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44,
  0xae, 0x42, 0x60, 0x82]);
if (!buf.subarray(buf.length - 12).equals(IEND)) {
  fail("entry.png has no IEND chunk: truncated PNG");
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  fail(`entry.png must be 1024x1024, got ${width}x${height}`);
}
const sha = createHash("sha256").update(buf).digest("hex");
if (sha !== ENTRY_SHA256) fail(`entry.png sha256 mismatch: got ${sha}`);

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(ENTRY, join(outDir, "entry.png"));
console.log(`wrote ${join(outDir, "entry.png")}: ${buf.length} bytes, sha256 ${sha}`);
