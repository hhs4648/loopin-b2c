import { defineConfig, loadEnv, type Plugin } from "vite";
import react from "@vitejs/plugin-react";
import fs from "node:fs";
import path from "node:path";

/** A VITE_ key is copied into the public site if any screen reads it. Refuse a production build that would publish the model key. */
function refuseClientSecret(): Plugin {
  return {
    name: "refuse-client-secret",
    config(_config, env) {
      if (env.mode !== "production") return;
      const loaded = loadEnv(env.mode, process.cwd(), "VITE_");
      const key = loaded.VITE_ANTHROPIC_API_KEY?.trim();
      if (!key) return;
      const mentioned = walk("src").some((file) =>
        fs.readFileSync(file, "utf8").includes("import.meta.env.VITE_ANTHROPIC_API_KEY"),
      );
      if (mentioned) {
        throw new Error("VITE_ANTHROPIC_API_KEY would be published in the site. Remove it from the production build.");
      }
    },
  };
}

function walk(dir: string): string[] {
  const out: string[] = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full));
    else if (/\.(ts|tsx|js|jsx)$/.test(entry.name)) out.push(full);
  }
  return out;
}

export default defineConfig({
  plugins: [react(), refuseClientSecret()],
  build: {
    sourcemap: false,
    minify: "esbuild",
  },
  esbuild: {
    legalComments: "none",
    drop: ["debugger"],
  },
  // 폰으로 바로 보기 — Cloudflare 임시 터널(https://….trycloudflare.com)로 개발 서버를 열 때 그 주소를 허용한다
  server: {
    allowedHosts: [".trycloudflare.com"],
  },
});
