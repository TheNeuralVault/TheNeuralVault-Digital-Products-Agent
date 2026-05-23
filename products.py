#!/usr/bin/env python3
"""
TheNeuralVault-Digital-Products-Agent
Closes the loop from intelligence to revenue.
Designs digital products from validated demand signals.
Five-tier provenance on every product claim.
Operator builds and lists — this agent never publishes.
"""

import os
import sys
from datetime import datetime
from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"]
)

PRODUCT_TYPES = {
    "template": "Notion template or template bundle",
    "ebook": "Ebook guide or structured reference document",
    "prompt-pack": "Curated prompt pack for a specific use case",
    "swipe-file": "Swipe file or resource library",
    "bundle": "Bundle combining multiple product types",
}

SYSTEM_PROMPT = """You are TheNeuralVault-Digital-Products-Agent.
You design digital products that close the loop from intelligence to revenue.
You read validated demand signals and design specific, buildable products.

TheNeuralVault brand voice — Think Human. Act AI:
- Visionary but grounded
- Resourceful — maximum value, minimal complexity
- Principled — transparent provenance on everything
- Empowering — gives buyers tools they can use immediately

Product doctrine:
- Products solve specific problems for specific people
- The product name IS the SEO keyword
- Specific beats generic — always
- First product ships fast — perfect is the enemy of revenue
- Bundles have higher perceived value than single products
- One $17 sale proves the system — then scale

Price architecture:
- Single templates: $7-$17
- Ebook guides: $17-$37
- Prompt packs: $9-$27
- Bundles: $27-$97

Five-tier provenance for product claims:
T1 VERIFIED    — actual sales data (post-launch only)
T2 EXTRACTED   — from primary marketplace research with URL
T3 INFERRED    — converging demand signals from SEO + intel
T4 MODELED     — projected revenue/conversion (always disclose)
T5 FOUNDATIONAL— core product principle

Rules you cannot break:
- Tag every revenue projection T4 MODELED and disclose it
- Flag DEFAULT for thin demand evidence
- Flag CONFLICT for contradicting signals
- Never promise specific revenue outcomes
- Operator builds the product — you design the blueprint
- Operator creates all listings — you write the copy

Output format — follow exactly:

---
# PRODUCT BRIEF — [PRODUCT NAME]
**Status:** PENDING OPERATOR APPROVAL
**Date:** [date]
**Type:** [product type]
**Recommended Price:** $[price]
**Platform:** Gumroad (primary) / Lemon Squeezy (for tax handling)

---
## DEMAND VALIDATION
[Evidence this product has real demand — tag T1-T5]
[Confidence level: HIGH / MEDIUM / LOW]

---
## PRODUCT STRUCTURE
### Title (SEO keyword as product name)
[Exact title — this is the Gumroad listing title]

### Subtitle
[One sentence benefit statement]

### What's Included
[Complete list of deliverables with descriptions]

### Structure / Table of Contents
[Full outline — every section, page, or template tab]

---
## GUMROAD LISTING COPY

### Title
[SEO-optimized, under 60 characters]

### Short Description (under 150 characters)
[For search results and previews]

### Full Description (300-500 words)
[Complete Gumroad listing copy in TheNeuralVault brand voice]
[Benefit-led, specific, no hype]

### Tags (10 tags for Gumroad search)
[tag1, tag2, tag3, ...]

### Recommended Price
$[price] — rationale: [T4 MODELED — projected based on comparable products]

---
## DELIVERY EMAIL SEQUENCE (3 emails)

### Email 1 — Immediate delivery (send on purchase)
Subject: [subject]
Body: [complete email — under 150 words]

### Email 2 — Day 3 follow-up
Subject: [subject]
Body: [complete email — under 150 words — tips for getting max value]

### Email 3 — Day 7 upsell
Subject: [subject]
Body: [complete email — under 150 words — introduce next product]

---
## REVENUE PROJECTION
[T4 MODELED — always disclosed as estimate]
- Price: $[X]
- Estimated monthly sales: [N] units
- Estimated monthly revenue: $[X × N]
- Time to first sale target: [X days]
- Note: All projections are T4 MODELED estimates.
  Actual results depend on distribution and audience size.

---
## PROVENANCE REPORT
[Every factual claim tagged T1-T5]
[DEFAULT flags with resolution path]
[CONFLICT flags if any]

---
## OPERATOR BUILD CHECKLIST
- [ ] Product structure approved
- [ ] Price approved
- [ ] Gumroad listing copy approved
- [ ] Product built (Notion / Google Docs / Canva)
- [ ] Gumroad account set up at gumroad.com
- [ ] Listing created manually on Gumroad
- [ ] Delivery emails configured in Gumroad
- [ ] Product published: YES / NO
- [ ] Link shared in next Newsletter issue: YES / NO
---"""

def read_file_bounded(path, max_chars=1500):
    """Read file with bounded context"""
    if path and os.path.exists(path):
        with open(path, "r") as f:
            content = f.read()
        if len(content) > max_chars:
            return content[:max_chars] + "\n[Truncated — bounded context]"
        return content
    return None

def generate_product_brief(product_type, product_desc, intel, seo, brand):
    """Generate product brief — fresh bounded context per call"""
    print(f"\nDesigning: {product_type}...")

    context_parts = []
    if intel:
        context_parts.append(f"MARKET INTELLIGENCE (demand signals):\n{intel}")
    if seo:
        context_parts.append(f"SEO BRIEF (keyword targets — use as product names):\n{seo}")
    if brand:
        context_parts.append(f"BRAND BIBLE (voice and tone):\n{brand}")

    context = "\n\n---\n\n".join(context_parts) if context_parts else "No upstream context — design from TheNeuralVault philosophy and digital product best practices."

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"""Design a complete digital product brief for TheNeuralVault.

Product type: {product_type} — {product_desc}
Date: {datetime.now().strftime('%Y-%m-%d')}

Federation intelligence (use to validate demand):
{context}

Requirements:
- Identify the single highest-opportunity product to build right now
- Use SEO keywords as the exact product name
- Complete product structure with full outline
- Complete Gumroad listing copy ready to paste
- Three-email delivery sequence
- Revenue projection tagged T4 MODELED
- Full provenance report
- Complete operator build checklist

First Product Principle: Ship the simplest version of the
highest-demand product. One real sale beats ten perfect
unpublished products. Design for speed to market.

Tag every claim T1-T5. Flag DEFAULT for thin evidence.
Flag CONFLICT for contradicting signals.
All revenue projections must be tagged T4 MODELED."""
        }
    ]

    result = ""
    completion = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b",
        messages=messages,
        temperature=0.5,
        max_tokens=3500,
        stream=True
    )

    for chunk in completion:
        if not chunk.choices:
            continue
        if chunk.choices[0].delta.content is not None:
            text = chunk.choices[0].delta.content
            print(text, end="", flush=True)
            result += text

    print(f"\n[✓] {product_type} brief complete.")
    return result

def main():
    product_type = sys.argv[1] if len(sys.argv) > 1 else "template"
    output_file = sys.argv[2] if len(sys.argv) > 2 else f"products/brief-{product_type}-{datetime.now().strftime('%Y%m%d-%H%M')}.md"
    intel_path = sys.argv[3] if len(sys.argv) > 3 else None
    seo_path = sys.argv[4] if len(sys.argv) > 4 else None
    brand_path = sys.argv[5] if len(sys.argv) > 5 else None

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    if product_type not in PRODUCT_TYPES and product_type != "all":
        print(f"Unknown type: {product_type}")
        print(f"Available: {', '.join(PRODUCT_TYPES.keys())}, all")
        sys.exit(1)

    print("=" * 60)
    print("TheNeuralVault-Digital-Products-Agent")
    print(f"Product type: {product_type}")
    print(f"Started: {timestamp}")
    print("Five-tier provenance: ACTIVE")
    print("Revenue projections: T4 MODELED only")
    print("=" * 60)

    intel = read_file_bounded(intel_path, 1200)
    seo = read_file_bounded(seo_path, 1200)
    brand = read_file_bounded(brand_path, 800)

    print(f"Intel loaded:  {'YES' if intel else 'NO'}")
    print(f"SEO loaded:    {'YES' if seo else 'NO'}")
    print(f"Brand loaded:  {'YES' if brand else 'NO'}")

    if product_type == "all":
        targets = PRODUCT_TYPES
    else:
        targets = {product_type: PRODUCT_TYPES[product_type]}

    all_results = []
    conflicts = []
    defaults = []

    for ptype, pdesc in targets.items():
        result = generate_product_brief(ptype, pdesc, intel, seo, brand)
        all_results.append((ptype, result))
        if "CONFLICT" in result.upper():
            conflicts.append(ptype)
        if "DEFAULT" in result.upper():
            defaults.append(ptype)

    # Write output
    os.makedirs(
        os.path.dirname(output_file) if os.path.dirname(output_file) else "products",
        exist_ok=True
    )

    with open(output_file, "w") as f:
        f.write(f"# TheNeuralVault Digital Product Brief\n")
        f.write(f"**Date:** {timestamp}\n")
        f.write(f"**Agent:** TheNeuralVault-Digital-Products-Agent v1.0\n")
        f.write(f"**Type:** {product_type}\n")
        f.write(f"**Status:** PENDING OPERATOR APPROVAL\n")
        f.write(f"**Conflicts:** {len(conflicts)}\n")
        f.write(f"**Defaults:** {len(defaults)}\n\n")
        f.write("---\n\n")
        f.write("> OPERATOR: Review product structure, approve price,\n")
        f.write("> build the product, then create Gumroad listing manually.\n")
        f.write("> This agent never publishes. You always list and publish.\n\n")
        f.write("---\n\n")

        for ptype, result in all_results:
            f.write(result)
            f.write("\n\n---\n\n")

        if conflicts:
            f.write("## CONFLICTS — Operator Resolution Required\n")
            for c in conflicts:
                f.write(f"- {c}\n")
            f.write("\n")
        if defaults:
            f.write("## DEFAULTS — Thin Evidence Disclosed\n")
            for d in defaults:
                f.write(f"- {d}\n")

    print("\n" + "=" * 60)
    print(f"Brief saved: {output_file}")
    print("STATUS: PENDING OPERATOR APPROVAL")
    print("NEXT: Review → Build → List on Gumroad → Promote in Newsletter")
    if conflicts:
        print(f"⚠ CONFLICTS: {', '.join(conflicts)}")
    if defaults:
        print(f"◈ DEFAULTS: {', '.join(defaults)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
