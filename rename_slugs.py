#!/usr/bin/env python3
"""
Lightside slug rename script
- Renames HTML files
- Renames hero images following [slug]-hero.webp convention
- Updates all internal slug references across every HTML file
- Reports image references that don't follow the convention (manual rename needed)
- Reports any remaining old slug references post-run

Run from the root of the cloned repo:
    python3 rename_slugs.py --dry-run   (preview only, no changes)
    python3 rename_slugs.py             (execute)
"""

import os
import sys
from pathlib import Path

DRY_RUN = '--dry-run' in sys.argv

SLUG_MAP = {
    'mr-and-mrs-b-personal-guarantees':         'personal-guarantee-will-i-lose-my-home',
    'mr-jb-hmrc':                               'self-employed-tax-debt-cant-pay-hmrc',
    'mr-bb-divorce-and-debt':                   'divorce-who-is-responsible-for-joint-debt',
    'cau-ltd-closing-a-company':                'can-i-dissolve-company-instead-of-liquidation',
    'cc-ltd-business-turnaround':               'director-personal-debt-causing-business-cashflow-problems',
    'mr-g-personal-liability':                  'bankruptcy-order-annulled-cancelled-annulment',
    'ms-j-too-much-debt':                       'stuck-in-debt-cycle-using-credit-to-pay-credit',
    'ms-jj-too-much-debt':                      'separation-divorce-too-much-debt',
    'ms-j-your-property-at-risk':               'unsecured-debt-stopping-my-remortgage',
    'mr-a-bankruptcy':                          'business-debt-not-mine-hmrc-bankruptcy',
    'mr-a-personal-liability':                  'business-debt-not-mine-hmrc-bankruptcy',
    'mr-and-mrs-c-personal-too-much-debt':      'i-need-help-pg-personal-guarantee',
    'mr-n-too-much-debt':                       'can-i-settle-my-debts-for-less',
    'nim-ltd-personal-liability':               'what-do-i-do-about-a-directors-loan-account',
    'nim-ltd-closing-a-company':                'what-do-i-do-about-a-directors-loan-account',
    'ms-pa-business-personal-guarantees':       'breathing-space-stop-bankruptcy-personal-guarantee-settled',
    'mr-and-mrs-tac-property-at-risk':          'charging-order-on-house-what-are-my-options',
    'ms-r-divorce-debt':                        'can-i-keep-my-rental-property-if-i-go-bankrupt',
    'mr-cr-hmrc':                               'will-i-lose-my-buy-to-let-property-in-bankruptcy',
    'mrs-ss-property-at-risk':                  'will-i-lose-my-house-if-i-go-bankrupt',
    'gg-property-portfolio':                    'cant-afford-buy-to-let-mortgages-what-happens',
    'mr-d-and-mr-j-personal-liability':         'hmrc-vat-fraud-assessment-personal-liability-directors',
    'mr-and-mrs-v-bankruptcy':                  'mortgage-shortfall-after-repossession-what-happens',
    'mr-and-mrs-v-too-much-debt':               'debt-growing-despite-making-payments',
    'mr-v-other-situations':                    'debt-stopping-house-sale',
    'ms-m-creditors-bailiffs':                  'facing-prison-for-debt-can-it-be-stopped',
    'ken-personal-liability':                   'challenge-directors-loan-account-claim-from-liquidator',
    'mr-s-personal-liability':                  'directors-disqualification-director-ban',
    'sam-closing-a-company':                    'prepack-administration-save-business-close-company',
    'diana-closing-a-company':                  'bounce-back-loan-cant-repay',
    'jeff-death-debt':                          'parent-died-with-debts-is-family-home-at-risk',
    'david-debt-and-death':                     'how-do-i-deal-with-debt-person-who-died',
    '200SB-debt-and-death':                     'insolvent-estate-family-loan-will-it-be-repaid',
}

# These old slugs are aliases — they map to the same new file as another entry.
# Skip HTML rename for these; still replace references.
ALIAS_ONLY = {'mr-a-personal-liability', 'nim-ltd-closing-a-company'}

def log(msg):
    print(f"{'[DRY-RUN] ' if DRY_RUN else ''}{msg}")

def main():
    repo_root = Path('.').resolve()
    html_files = sorted(repo_root.glob('*.html'))

    if not html_files:
        print("ERROR: No HTML files found. Run from the repo root.")
        sys.exit(1)

    print(f"Repo root:      {repo_root}")
    print(f"HTML files:     {len(html_files)}")
    print(f"Mode:           {'DRY RUN — no changes' if DRY_RUN else 'LIVE EXECUTE'}\n")

    # ── PHASE 1: Rename HTML files ─────────────────────────────────────────────
    print("=" * 60)
    print("PHASE 1: Rename HTML files")
    print("=" * 60)

    for old_slug, new_slug in SLUG_MAP.items():
        if old_slug in ALIAS_ONLY:
            continue
        old_path = repo_root / f"{old_slug}.html"
        new_path = repo_root / f"{new_slug}.html"
        if not old_path.exists():
            log(f"  MISSING (skip): {old_slug}.html")
            continue
        if new_path.exists():
            log(f"  CONFLICT (skip): {new_slug}.html already exists")
            continue
        log(f"  RENAME: {old_slug}.html → {new_slug}.html")
        if not DRY_RUN:
            old_path.rename(new_path)

    # ── PHASE 2: Rename [slug]-hero.webp images ────────────────────────────────
    print(f"\n{'=' * 60}")
    print("PHASE 2: Rename [slug]-hero.webp images")
    print("=" * 60)

    for old_slug, new_slug in SLUG_MAP.items():
        if old_slug in ALIAS_ONLY:
            continue
        old_img = repo_root / f"{old_slug}-hero.webp"
        if old_img.exists():
            new_img = repo_root / f"{new_slug}-hero.webp"
            log(f"  RENAME: {old_img.name} → {new_img.name}")
            if not DRY_RUN:
                old_img.rename(new_img)
        else:
            log(f"  NO HERO IMG: {old_slug}-hero.webp (not found — may need manual rename)")

    # ── PHASE 3: Update all slug references in all HTML files ─────────────────
    print(f"\n{'=' * 60}")
    print("PHASE 3: Update slug references in all HTML files")
    print("=" * 60)

    all_html = sorted(repo_root.glob('*.html'))
    total_replacements = 0

    for html_path in all_html:
        try:
            content = html_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  ERROR reading {html_path.name}: {e}")
            continue

        original = content
        file_replacements = 0

        # Longest slugs first to avoid partial matches
        for old_slug in sorted(SLUG_MAP.keys(), key=len, reverse=True):
            new_slug = SLUG_MAP[old_slug]
            count = content.count(old_slug)
            if count:
                content = content.replace(old_slug, new_slug)
                file_replacements += count
                log(f"  {html_path.name}: '{old_slug}' → '{new_slug}' ({count}x)")

        if file_replacements > 0:
            total_replacements += file_replacements
            if not DRY_RUN:
                html_path.write_text(content, encoding='utf-8')

    print(f"\n  Total replacements: {total_replacements}")

    # ── PHASE 4: Report image references needing manual rename ────────────────
    print(f"\n{'=' * 60}")
    print("PHASE 4: Image references not following [slug]-hero.webp convention")
    print("(These need manual rename in GitHub)")
    print("=" * 60)

    all_html = sorted(repo_root.glob('*.html'))
    manual_images = {}

    for html_path in all_html:
        try:
            content = html_path.read_text(encoding='utf-8')
        except:
            continue
        # Find all webp references
        import re
        imgs = re.findall(r'["\']([^"\']*\.webp)["\']', content)
        for img in imgs:
            img_name = img.split('/')[-1]
            # Check if this image corresponds to an old slug but doesn't follow -hero convention
            for old_slug, new_slug in SLUG_MAP.items():
                if old_slug in img_name and not img_name == f"{old_slug}-hero.webp":
                    if img_name not in manual_images:
                        manual_images[img_name] = new_slug

    if manual_images:
        print(f"  {'Image filename':<50} {'Rename to'}")
        print(f"  {'-'*49} {'-'*49}")
        for old_img, new_slug in sorted(manual_images.items()):
            # Derive new image name by replacing old slug portion
            new_img = old_img
            for old_slug in sorted(SLUG_MAP.keys(), key=len, reverse=True):
                if old_slug in old_img:
                    new_img = old_img.replace(old_slug, SLUG_MAP[old_slug])
                    break
            print(f"  {old_img:<50} → {new_img}")
    else:
        print("  None found — all image references follow the convention or have no old slugs.")

    # ── PHASE 5: Verification — scan for remaining old slugs ──────────────────
    print(f"\n{'=' * 60}")
    print("PHASE 5: Verification — scanning for remaining old slug references")
    print("=" * 60)

    remaining = []
    for html_path in sorted(repo_root.glob('*.html')):
        try:
            content = html_path.read_text(encoding='utf-8')
        except:
            continue
        for old_slug in SLUG_MAP.keys():
            if old_slug in content:
                remaining.append((html_path.name, old_slug))

    if remaining:
        print(f"  ⚠️  OLD SLUGS STILL PRESENT ({len(remaining)}):")
        for fname, slug in remaining:
            print(f"     {fname}: '{slug}'")
    else:
        print("  ✅ Clean — no old slug references remain.")

    print(f"\n{'=' * 60}")
    print("DONE" if not DRY_RUN else "DRY RUN COMPLETE — no files changed")
    print("=" * 60)

if __name__ == '__main__':
    main()
