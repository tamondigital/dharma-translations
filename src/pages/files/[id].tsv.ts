import type { APIRoute } from "astro";
import { texts } from "../../lib/data";

export function getStaticPaths() {
  return texts.map((t) => ({ params: { id: t.id }, props: { tsv: t.tsv } }));
}
export const GET: APIRoute = ({ props }) =>
  new Response(props.tsv as string, { headers: { "Content-Type": "text/tab-separated-values; charset=utf-8" } });
