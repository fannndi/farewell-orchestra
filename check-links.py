#!/usr/bin/env python3
"""
Link checker for Markdown files.
Scans all .md files in the repo, extracts links, and validates them.
"""

import asyncio
import asyncio.exceptions
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, urljoin
import aiohttp
import asyncio.exceptions


# Regex to match markdown links: [text](url)
MD_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

# Regex to match bare URLs (http/https)
BARE_URL_RE = re.compile(r'(?<!\]\()https?://[^\s\)]+')


async def check_url(session: aiohttp.ClientSession, url: str, timeout: int = 10) -> tuple[str, int | None, str]:
    """Check a single URL, return (url, status_code, error_message)."""
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        return url, None, f"skipped (scheme: {parsed.scheme})"

    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout), allow_redirects=True) as resp:
            return url, resp.status, ""
    except asyncio.TimeoutError:
        return url, None, f"timeout ({timeout}s)"
    except aiohttp.ClientError as e:
        return url, None, str(e)
    except asyncio.exceptions.CancelledError:
        raise
    except Exception as e:
        return url, None, f"{type(e).__name__}: {e}"


def extract_links(filepath: Path) -> list[tuple[str, int, str]]:
    """Extract all links from a markdown file. Returns list of (url, line_number, context)."""
    links = []
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
        return links

    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        # Markdown links: [text](url)
        for match in MD_LINK_RE.finditer(line):
            url = match.group(2).strip()
            if url and not url.startswith('#'):  # Skip anchor links
                links.append((url, i, line.strip()[:80]))

        # Bare URLs (not in markdown links)
        # Only match if not already inside a markdown link
        for match in BARE_URL_RE.finditer(line):
            url = match.group(0).rstrip('.,;)')
            # Check if this URL is inside a markdown link
            before = line[:match.start()]
            if '](' in before and ')' not in before[before.rindex('](')+2:]:
                continue  # inside a markdown link, skip
            links.append((url, i, line.strip()[:80]))

    return links


async def check_links_in_file(session: aiohttp.ClientSession, filepath: Path, semaphore: asyncio.Semaphore) -> list[tuple[str, int, str, int | None, str]]:
    """Check all links in a single file. Returns list of (url, line, context, status, error)."""
    links = extract_links(filepath)
    if not links:
        return []

    results = []

    async def check_one(url: str, line: int, context: str):
        async with semaphore:
            url, status, error = await check_url(session, url)
            return url, line, context, status, error

    tasks = [check_one(url, line, ctx) for url, line, ctx in links]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for r in results:
        if isinstance(r, Exception):
            print(f"  Error checking link: {r}", file=sys.stderr)
        else:
            results.append(r)

    return results


async def main():
    repo_root = Path(__file__).parent
    md_files = list(repo_root.rglob('*.md'))

    if not md_files:
        print("No markdown files found.")
        return 0

    print(f"Scanning {len(md_files)} markdown file(s)...")

    # Limit concurrent connections
    semaphore = asyncio.Semaphore(10)

    async with aiohttp.ClientSession(
        headers={'User-Agent': 'farewell-orchestra-link-checker/1.0'}
    ) as session:

        all_results = []
        for md_file in md_files:
            rel_path = md_file.relative_to(repo_root)
            print(f"\nChecking {rel_path}...")
            results = await check_links_in_file(session, md_file, semaphore)
            for url, line, context, status, error in results:
                all_results.append((str(rel_path), url, line, context, status, error))

    # Report results
    failed = []
    skipped = []
    passed = []

    for rel_path, url, line, context, status, error in all_results:
        if error:
            if 'skipped' in error.lower():
                skipped.append((rel_path, url, line, context, error))
            else:
                failed.append((rel_path, url, line, context, error))
        elif status and 200 <= status < 400:
            passed.append((rel_path, url, line, context, status))
        else:
            failed.append((rel_path, url, line, context, f"HTTP {status}" if status else "unknown error"))

    # Summary
    print("\n" + "=" * 60)
    print("LINK CHECK SUMMARY")
    print("=" * 60)
    print(f"Total links checked: {len(all_results)}")
    print(f"Passed: {len(passed)}")
    print(f"Failed: {len(failed)}")
    print(f"Skipped: {len(skipped)}")

    if failed:
        print("\nFAILED LINKS:")
        print("-" * 60)
        for rel_path, url, line, context, error in failed:
            print(f"  {rel_path}:{line}: {url}")
            print(f"    Error: {error}")
            print(f"    Context: {context}")

    if skipped:
        print("\nSKIPPED LINKS (non-HTTP):")
        print("-" * 60)
        for rel_path, url, line, context, reason in skipped:
            print(f"  {rel_path}:{line}: {url} ({reason})")

    if failed:
        print(f"\nFAILED: {len(failed)} broken link(s)")
        return 1

    print("\nAll links OK!")
    return 0


if __name__ == '__main__':
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)