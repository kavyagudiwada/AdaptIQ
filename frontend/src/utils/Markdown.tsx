/**
 * Minimal markdown-to-JSX renderer.
 *
 * The tutor returns markdown, but pulling in a full parser is unnecessary for
 * an MVP. This handles the subset we actually emit: headings, bold, inline
 * code, fenced code blocks, bullet lists, paragraphs, and inline / display
 * mathematics written in LaTeX delimiters ($...$ and $$...$$).
 */
import { Fragment, type ReactNode } from "react";
import katex from "katex";
import "katex/dist/katex.min.css";

const KATEX_OPTIONS = {
  throwOnError: false,
  strict: false,
};

/** Render one LaTeX snippet (without the surrounding $ markers). */
function renderMath(latex: string, display: boolean): ReactNode {
  const html = katex.renderToString(latex, {
    ...KATEX_OPTIONS,
    displayMode: display,
  });
  return (
    <span
      // KaTeX typesets into the HTML we generate above; the outer span is a
      // stable mount point so we never need dangerouslySetInnerHTML twice.
      className={display ? "katex-display block" : "katex-inline"}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

/**
 * Split a line into plain text / code / bold / inline-math segments.
 *
 * Order matters: code first so ** or $ inside backticks is left alone, bold
 * before math so equations containing `**` still parse, inline math last so we
 * match the shortest `$...$` span on the line.
 */
function renderInline(text: string, keyPrefix: string): ReactNode[] {
  const nodes: ReactNode[] = [];
  const pattern = /(`[^`]+`)|(\*\*[^*]+\*\*)|(\$[^$`]+\$)/g;
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
    } else if (token.startsWith("**")) {
      nodes.push(
        <strong key={`${keyPrefix}-b${i}`} className="font-semibold text-ink-900">
          {token.slice(2, -2)}
        </strong>,
      );
    } else {
      nodes.push(
        <Fragment key={`${keyPrefix}-m${i}`}>
          {renderMath(token.slice(1, -1), false)}
        </Fragment>,
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
  let mathBuffer: string[] = [];

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

  const flushMath = (key: string) => {
    if (mathBuffer.length === 0) return;
    out.push(
      <div key={key} className="my-3 flex justify-center">
        {renderMath(
          mathBuffer.join("\n").replace(/^\$\$|\$\$$/g, "").trim(),
          true,
        )}
      </div>,
    );
    mathBuffer = [];
  };

  blocks.forEach((raw, idx) => {
    const line = raw.replace(/\s+$/, "");

    if (line.trim().startsWith("```")) {
      flushList(`ul-${idx}`);
      flushMath(`math-${idx}`);
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
        inCode = true;
      }
      return;
    }

    if (inCode) {
      codeBuffer.push(raw);
      return;
    }

    // A line wholly wrapped in $$...$$ is a display equation.
    const trimmed = line.trim();
    if (trimmed.startsWith("$$") && trimmed.endsWith("$$") && trimmed.length > 4) {
      flushList(`ul-${idx}`);
      out.push(
        <div key={`math-${idx}`} className="my-3 flex justify-center">
          {renderMath(trimmed.slice(2, -2).trim(), true)}
        </div>,
      );
      return;
    }
    // Opening line of a multi-line $$ block.
    if (trimmed.startsWith("$$")) {
      flushList(`ul-${idx}`);
      mathBuffer.push(trimmed);
      return;
    }
    if (mathBuffer.length > 0) {
      mathBuffer.push(trimmed);
      if (trimmed.endsWith("$$")) {
        flushMath(`math-${idx}`);
      }
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
  flushMath("math-end");
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