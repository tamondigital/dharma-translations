import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// GitHub Pages project site at https://tiedy.com/dharma-translations/ (custom domain on the tamondigital.github.io root repo).
// The repo name is the path: renaming the repo moves every URL.
export default defineConfig({
  site: "https://tiedy.com",
  base: "/dharma-translations",
  trailingSlash: "always",
  build: { format: "directory" },
  integrations: [sitemap()],
});
