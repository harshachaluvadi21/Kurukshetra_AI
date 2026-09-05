import React from 'react';

/**
 * Converts raw markdown+backend labels into clean HTML-rendered React nodes.
 * Handles:
 * - [FACT], [ESTIMATE], [MODEL ASSUMPTION], [PROPOSED TARGET] → badges
 * - > [!NOTE], > [!IMPORTANT], > [!WARNING], > [!TIP] → callouts
 * - **bold** → <strong>
 * - ## headings → styled h elements
 * - - bullets → styled list items
 * - Removes raw internal formatting symbols
 */

/** Strip and replace classification tags with badge markup */
function processClassificationTags(line: string): string {
  return line
    .replace(/\[FACT[^\]]*\]/gi, '<span class="badge badge-fact" style="margin-left:6px">Verified</span>')
    .replace(/\[ESTIMATE[^\]]*\]/gi, '<span class="badge badge-estimate" style="margin-left:6px">Estimate</span>')
    .replace(/\[MODEL ASSUMPTION[^\]]*\]/gi, '<span class="badge badge-assumption" style="margin-left:6px">Assumption</span>')
    .replace(/\[ASSUMPTION[^\]]*\]/gi, '<span class="badge badge-assumption" style="margin-left:6px">Assumption</span>')
    .replace(/\[PROPOSED TARGET[^\]]*\]/gi, '<span class="badge badge-target" style="margin-left:6px">Target</span>')
    .replace(/\[TARGET[^\]]*\]/gi, '<span class="badge badge-target" style="margin-left:6px">Target</span>');
}

/** Convert **bold** to <strong> and *italic* to <em> */
function processInlineFormatting(text: string): string {
  return text
    .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>');
}

/** Process a line to full HTML */
function processLine(line: string): string {
  return processClassificationTags(processInlineFormatting(line));
}

interface Block {
  type: 'h1' | 'h2' | 'h3' | 'h4' | 'bullet' | 'numbered' | 'paragraph' | 'hr' | 'callout' | 'empty';
  content: string;
  calloutType?: string;
}

function parseBlocks(markdown: string): Block[] {
  const lines = markdown.split('\n');
  const blocks: Block[] = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    // Callout > [!NOTE] etc.
    if (trimmed.startsWith('> [!')) {
      const calloutMatch = trimmed.match(/^> \[!(\w+)\]/);
      const calloutType = calloutMatch?.[1]?.toLowerCase() || 'note';
      const contentLines: string[] = [];
      i++;
      while (i < lines.length && lines[i].trim().startsWith('> ')) {
        contentLines.push(lines[i].trim().replace(/^>\s*/, ''));
        i++;
      }
      blocks.push({ type: 'callout', content: contentLines.join(' '), calloutType });
      continue;
    }

    // Skip lines that are just the data classification standard note
    if (trimmed.includes('Data Classification Standard') && trimmed.includes('FACTS')) {
      i++;
      continue;
    }

    // Headings
    if (trimmed.startsWith('#### ')) { blocks.push({ type: 'h4', content: processLine(trimmed.slice(5)) }); i++; continue; }
    if (trimmed.startsWith('### '))  { blocks.push({ type: 'h3', content: processLine(trimmed.slice(4)) }); i++; continue; }
    if (trimmed.startsWith('## '))   { blocks.push({ type: 'h2', content: processLine(trimmed.slice(3)) }); i++; continue; }
    if (trimmed.startsWith('# '))    { blocks.push({ type: 'h1', content: processLine(trimmed.slice(2)) }); i++; continue; }

    // HR
    if (/^---+$/.test(trimmed) || /^\*\*\*+$/.test(trimmed)) {
      blocks.push({ type: 'hr', content: '' }); i++; continue;
    }

    // Bullet
    if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
      blocks.push({ type: 'bullet', content: processLine(trimmed.slice(2)) }); i++; continue;
    }

    // Numbered list
    if (/^\d+\.\s/.test(trimmed)) {
      blocks.push({ type: 'numbered', content: processLine(trimmed.replace(/^\d+\.\s/, '')) }); i++; continue;
    }

    // Empty line
    if (!trimmed) { blocks.push({ type: 'empty', content: '' }); i++; continue; }

    // Paragraph
    blocks.push({ type: 'paragraph', content: processLine(trimmed) });
    i++;
  }

  return blocks;
}

interface MarkdownRendererProps {
  content: string | undefined | null;
  /** If true, suppress the leading heading that matches the section title */
  suppressTitle?: string;
  className?: string;
}

export function MarkdownRenderer({ content, suppressTitle, className = '' }: MarkdownRendererProps) {
  if (!content) {
    return (
      <p style={{ fontSize: 14, color: 'var(--text-tertiary)', fontStyle: 'italic' }}>
        Not yet generated.
      </p>
    );
  }

  const blocks = parseBlocks(content);

  // Suppress the leading heading if it matches suppressTitle
  let startIdx = 0;
  if (suppressTitle && blocks.length > 0) {
    const first = blocks[0];
    if ((first.type === 'h1' || first.type === 'h2') && 
        first.content.toLowerCase().includes(suppressTitle.toLowerCase())) {
      startIdx = 1;
    }
  }

  const rendered: React.ReactNode[] = [];
  let bulletBuffer: string[] = [];
  let numberedBuffer: string[] = [];

  const flushBullets = (key: string) => {
    if (bulletBuffer.length > 0) {
      rendered.push(
        <ul key={key} style={{ margin: '8px 0 12px', padding: 0, listStyle: 'none' }}>
          {bulletBuffer.map((item, j) => (
            <li key={j} style={{ padding: '2px 0 2px 20px', position: 'relative', fontSize: 14, color: 'var(--text-secondary)', lineHeight: 1.7 }}>
              <span style={{ position: 'absolute', left: 0, color: 'var(--accent)', fontWeight: 700 }}>›</span>
              <span dangerouslySetInnerHTML={{ __html: item }} />
            </li>
          ))}
        </ul>
      );
      bulletBuffer = [];
    }
  };

  const flushNumbered = (key: string) => {
    if (numberedBuffer.length > 0) {
      rendered.push(
        <ol key={key} style={{ margin: '8px 0 12px', padding: 0, listStyle: 'none', counterReset: 'num' }}>
          {numberedBuffer.map((item, j) => (
            <li key={j} style={{ padding: '3px 0 3px 28px', position: 'relative', fontSize: 14, color: 'var(--text-secondary)', lineHeight: 1.7, counterIncrement: 'num' }}>
              <span style={{ position: 'absolute', left: 0, color: 'var(--accent)', fontWeight: 700, fontSize: 12 }}>{j + 1}.</span>
              <span dangerouslySetInnerHTML={{ __html: item }} />
            </li>
          ))}
        </ol>
      );
      numberedBuffer = [];
    }
  };

  blocks.slice(startIdx).forEach((block, idx) => {
    const key = `block-${idx}`;

    if (block.type === 'bullet') { bulletBuffer.push(block.content); return; }
    if (block.type === 'numbered') { numberedBuffer.push(block.content); return; }

    flushBullets(`bullets-${idx}`);
    flushNumbered(`numbered-${idx}`);

    switch (block.type) {
      case 'h1':
        rendered.push(<h2 key={key} style={{ fontSize: 18, fontWeight: 700, color: 'var(--text-primary)', margin: '24px 0 10px', paddingBottom: 8, borderBottom: '1px solid var(--border)' }} dangerouslySetInnerHTML={{ __html: block.content }} />);
        break;
      case 'h2':
        rendered.push(<h3 key={key} style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)', margin: '20px 0 8px' }} dangerouslySetInnerHTML={{ __html: block.content }} />);
        break;
      case 'h3':
        rendered.push(<h4 key={key} style={{ fontSize: 14, fontWeight: 600, color: 'var(--text-primary)', margin: '16px 0 6px' }} dangerouslySetInnerHTML={{ __html: block.content }} />);
        break;
      case 'h4':
        rendered.push(<p key={key} style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.07em', color: 'var(--text-secondary)', margin: '14px 0 4px' }} dangerouslySetInnerHTML={{ __html: block.content }} />);
        break;
      case 'hr':
        rendered.push(<hr key={key} style={{ border: 'none', borderTop: '1px solid var(--border)', margin: '20px 0' }} />);
        break;
      case 'callout': {
        const ctMap: Record<string, string> = { note: 'callout-note', important: 'callout-important', warning: 'callout-warning', tip: 'callout-tip' };
        const ctClass = ctMap[block.calloutType || 'note'] || 'callout-note';
        rendered.push(<div key={key} className={`callout ${ctClass}`} dangerouslySetInnerHTML={{ __html: block.content }} />);
        break;
      }
      case 'empty':
        // Don't add more than one consecutive empty space
        if (rendered.length > 0 && !((rendered[rendered.length - 1] as React.ReactElement)?.key?.startsWith?.('empty'))) {
          rendered.push(<div key={key} style={{ height: 6 }} />);
        }
        break;
      case 'paragraph':
      default:
        rendered.push(<p key={key} style={{ fontSize: 14, color: 'var(--text-secondary)', marginBottom: 8, lineHeight: 1.75 }} dangerouslySetInnerHTML={{ __html: block.content }} />);
    }
  });

  flushBullets('bullets-final');
  flushNumbered('numbered-final');

  return <div className={`report-prose ${className}`}>{rendered}</div>;
}

/**
 * Derives a short display name from a long business concept string.
 * Used when no explicit company/product name is available.
 */
export function deriveDisplayName(concept: string | null | undefined, maxLen = 40): string {
  if (!concept) return 'Startup Analysis';
  if (concept.length <= maxLen) return concept;
  // Take first 5 words max
  const words = concept.trim().split(/\s+/);
  const short = words.slice(0, 5).join(' ');
  return short.length < concept.length ? short + '…' : concept;
}

/**
 * Format large INR numbers naturally.
 * e.g. 1000000 → ₹10 Lakh, 10000000 → ₹1 Cr
 */
export function formatINR(value: number | null | undefined): string {
  if (value === null || value === undefined) return '—';
  if (value >= 10000000) return `₹${(value / 10000000).toFixed(1)} Cr`;
  if (value >= 100000) return `₹${(value / 100000).toFixed(1)} Lakh`;
  if (value >= 1000) return `₹${(value / 1000).toFixed(1)}K`;
  return `₹${value}`;
}
