#!/bin/bash
# TheNeuralVault-Digital-Products-Agent — Task Runner
# Usage: bash run-products.sh [product_type]
# Types: template, ebook, prompt-pack, swipe-file, bundle, all

PRODUCT_TYPE="${1:-template}"
TIMESTAMP=$(date +%Y-%m-%d-%H%M)
OUTPUT_FILE="products/brief-${PRODUCT_TYPE}-${TIMESTAMP}.md"
MEMORY_FILE="memory/products-log.md"

mkdir -p products memory intel briefs/brand briefs/seo

echo "============================================"
echo "TheNeuralVault-Digital-Products-Agent"
echo "Product Type: $PRODUCT_TYPE"
echo "Started: $TIMESTAMP"
echo "============================================"

# Pull all upstream intelligence from Drive
echo "Pulling federation intelligence from Drive..."
rclone copy NeuralVault:theneuralvault/intel/ intel/ --include "*.md"
rclone copy NeuralVault:theneuralvault/briefs/ briefs/ --include "*.md"
rclone copy NeuralVault:theneuralvault/briefs/brand/ briefs/brand/ --include "*.md"
rclone copy NeuralVault:theneuralvault/briefs/seo/ briefs/seo/ --include "*.md"

# Find latest inputs
LATEST_INTEL=$(ls -t intel/*.md 2>/dev/null | head -1)
LATEST_SEO=$(ls -t briefs/seo*.md briefs/seo/*.md 2>/dev/null | head -1)
LATEST_BRAND=$(ls -t briefs/brand/*.md 2>/dev/null | head -1)

echo "Intel:  ${LATEST_INTEL:-none}"
echo "SEO:    ${LATEST_SEO:-none}"
echo "Brand:  ${LATEST_BRAND:-none}"
echo ""

# Generate product brief
python3 products.py \
  "$PRODUCT_TYPE" \
  "$OUTPUT_FILE" \
  "$LATEST_INTEL" \
  "$LATEST_SEO" \
  "$LATEST_BRAND"

# Sync to Drive
echo ""
echo "Syncing to Drive..."
rclone copy products/ NeuralVault:theneuralvault/output/products/
rclone copy memory/ NeuralVault:theneuralvault/memory/digital-products/

# Log run
echo "$(date) | Type: $PRODUCT_TYPE | Brief: $OUTPUT_FILE" >> "$MEMORY_FILE"

echo ""
echo "============================================"
echo "Product brief complete."
echo "Saved: $OUTPUT_FILE"
echo "Synced: NeuralVault:theneuralvault/output/products/"
echo ""
echo "OPERATOR NEXT STEPS:"
echo "1. Open brief in Drive"
echo "2. Review and approve product structure"
echo "3. Build the product (Notion, Google Docs, Canva)"
echo "4. Create Gumroad listing using provided copy"
echo "5. Set price and publish"
echo "6. Share in next Newsletter issue"
echo "============================================"
