import fs from "node:fs/promises";
import path from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const require = createRequire(import.meta.url);
const { chromium } = require("/Users/zj/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");
const root = path.resolve(__dirname, "../../..");
const htmlPath = path.join(__dirname, "segment-01.html");
const outDir = path.join(root, "renders", "segment-01");
const frameDir = path.join(outDir, "frames");
const output = path.join(outDir, "segment-01-opening.mp4");
const poster = path.join(outDir, "segment-01-poster.png");

const width = 1920;
const height = 1080;
const fps = 30;
const duration = 16;
const totalFrames = fps * duration;

async function run(cmd, args) {
  await new Promise((resolve, reject) => {
    const child = spawn(cmd, args, { stdio: "inherit" });
    child.on("error", reject);
    child.on("close", (code) => {
      if (code === 0) resolve();
      else reject(new Error(`${cmd} exited with code ${code}`));
    });
  });
}

await fs.rm(outDir, { recursive: true, force: true });
await fs.mkdir(frameDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({
  viewport: { width, height },
  deviceScaleFactor: 1,
});
await page.goto(`file://${htmlPath}`);

for (let i = 0; i < totalFrames; i += 1) {
  const t = i / fps;
  await page.evaluate((time) => window.renderFrame(time), t);
  await page.screenshot({
    path: path.join(frameDir, `frame-${String(i).padStart(5, "0")}.png`),
    type: "png",
    animations: "disabled",
  });
  if (i === 390) {
    await page.screenshot({ path: poster, type: "png", animations: "disabled" });
  }
  if (i % 60 === 0) {
    console.log(`rendered ${i}/${totalFrames}`);
  }
}

await browser.close();

await run("ffmpeg", [
  "-y",
  "-framerate",
  String(fps),
  "-i",
  path.join(frameDir, "frame-%05d.png"),
  "-c:v",
  "libx264",
  "-pix_fmt",
  "yuv420p",
  "-profile:v",
  "high",
  "-crf",
  "18",
  "-movflags",
  "+faststart",
  output,
]);

console.log(output);
