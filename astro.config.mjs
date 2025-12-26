import { defineConfig } from "astro/config"
import icon from "astro-icon"
import remarkMath from "remark-math"
import rehypeKatex from "rehype-katex"

// https://astro.build/config
export default defineConfig({
  site: "https://dais.rhein-main-universitaeten.de",
  markdown: { remarkPlugins: [remarkMath], rehypePlugins: [rehypeKatex] },
  integrations: [icon()],
})
