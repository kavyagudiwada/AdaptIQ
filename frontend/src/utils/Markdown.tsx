/**
 * Minimal markdown-to-JSX renderer.
 *
 * The tutor returns markdown, but pulling in a full parser is unnecessary for
 * an MVP. This handles the subset we actually emit: headings, bold, inline
 * code, fenced code blocks, bullet lists and paragraphs.
 */
import { Fragment, type ReactNode } from "react";

function renderInline(text: string, keyPrefix: string): ReactNode[] {
  const nodes: ReactNode[] = [];
  // Order matters: code first so ** inside backticks is left alone.
  const pattern = /(`[^`]+`)|(\*\*[^*]+\*\*)/g;
  let last = 0;
  let match: RegExpExecArray | null;
  let i = 0;

  while ((match = pattern.exec(text)) !== null) {
    if (match.index > last) {
      nodes.push(text.slice(last, match.index));
    }
    const token = match[0];
    if (token.startsWith("`")) {
      nodes.push(
        <code
          key={`${keyPrefix}-c${i}`}
          className="rounded bg-ink-100 px-1.5 py-0.5 font-mono text-[0.85em] text-brand-800"
        >
          {token.slice(1, -1)}
        </code>,
      );
    } else {
      nodes.push(
        <strong key={`${keyPrefix}-b${i}`} className="font-semibold text-ink-900">
          {token.slice(2, -2)}
        </strong>,
      );
    }
    last = match.index + token.length;
    i += 1;
  }
  if (last < text.length) nodes.push(text.slice(last));
  return nodes;
}

export function Markdown({ text, className }: { text: string; className?: string }) {
  const blocks = text.split("\n");
  const out: ReactNode[] = [];
  let listBuffer: string[] = [];
  let inCode = false;
  let codeBuffer: string[] = [];

  const flushList = (key: string) => {
    if (listBuffer.length === 0) return;
    out.push(
      <ul key={key} className="my-2 list-disc space-y-1 pl-5">
        {listBuffer.map((item, idx) => (
          <li key={`${key}-${idx}`}>{renderInline(item, `${key}-${idx}`)}</li>
        ))}
      </ul>,
    );
    listBuffer = [];
  };

  blocks.forEach((raw, idx) => {
    const line = raw.replace(/\s+$/, "");

    if (line.trim().startsWith("```")) {
      if (inCode) {
        out.push(
          <pre
            key={`code-${idx}`}
            className="scroll-slim my-3 overflow-x-auto rounded-xl bg-ink-950 p-4 text-xs leading-relaxed text-ink-100"
          >
            <code>{codeBuffer.join("\n")}</code>
          </pre>,
        );
        codeBuffer = [];
        inCode = false;
      } else {
        flushList(`ul-${idx}`);
        inCode = true;
      }
      return;
    }

    if (inCode) {
      codeBuffer.push(raw);
      return;
    }

    if (!line.trim()) {
      flushList(`ul-${idx}`);
      return;
    }

    if (/^###\s+/.test(line)) {
      flushList(`ul-${idx}`);
      out.push(
        <h4 key={idx} className="mt-4 mb-1.5 text-sm font-bold text-ink-900">
          {renderInline(line.replace(/^###\s+/, ""), `h-${idx}`)}
        </h4>,
      );
      return;
    }
    if (/^##\s+/.test(line)) {
      flushList(`ul-${idx}`);
      out.push(
        <h3 key={idx} className="mt-4 mb-1.5 text-base font-bold text-ink-900">
          {renderInline(line.replace(/^##\s+/, ""), `h-${idx}`)}
        </h3>,
      );
      return;
    }
    if (/^#\s+/.test(line)) {
      flushList(`ul-${idx}`);
      out.push(
        <h2 key={idx} className="mt-4 mb-2 text-lg font-bold text-ink-900">
          {renderInline(line.replace(/^#\s+/, ""), `h-${idx}`)}
        </h2>,
      );
      return;
    }

    if (/^\s*[-*]\s+/.test(line)) {
      listBuffer.push(line.replace(/^\s*[-*]\s+/, ""));
      return;
    }

    flushList(`ul-${idx}`);
    out.push(
      <p key={idx} className="my-2 leading-relaxed first:mt-0 last:mb-0">
        {renderInline(line, `p-${idx}`)}
      </p>,
    );
  });

  flushList("ul-end");
  if (inCode && codeBuffer.length) {
    out.push(
      <pre key="code-tail" className="mt-3 overflow-x-auto rounded-xl bg-ink-950 p-4 text-xs text-ink-100">
        <code>{codeBuffer.join("\n")}</code>
      </pre>,
    );
  }

  return (
    <div className={className}>
      {out.map((node, idx) => (
        <Fragment key={idx}>{node}</Fragment>
      ))}
    </div>
  );
}
