#!/usr/bin/env bash
set -euo pipefail

# Ensure we're in a git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: not inside a Git repository."
  exit 1
fi

# # Check for uncommitted changes
# if ! git diff --quiet || ! git diff --cached --quiet; then
#   echo "Error: You have uncommitted changes. Please commit or stash them first."
#   exit 1
# fi

# Get last git tag (if any)
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

# Compute suggested next version
if [[ -n "$LAST_TAG" ]]; then
  # Detect prefix (like "v") and numeric part
  PREFIX=$(echo "$LAST_TAG" | grep -oE '^[^0-9]*')
  NUM_PART=$(echo "$LAST_TAG" | grep -oE '[0-9]+(\.[0-9]+)*$')

  # Split numeric parts into array
  IFS='.' read -r -a PARTS <<< "$NUM_PART"

  # Increment the last numeric part
  LAST_INDEX=$(( ${#PARTS[@]} - 1 ))
  PARTS[$LAST_INDEX]=$(( ${PARTS[$LAST_INDEX]} + 1 ))

  # Recombine version number
  NEXT_NUM=$(IFS='.'; echo "${PARTS[*]}")
  DEFAULT_VERSION="${PREFIX}${NEXT_NUM}"
else
  DEFAULT_VERSION=""
fi

# Ask for version, with auto-suggested default
read -rp "Enter new version [default: $DEFAULT_VERSION]: " VERSION
VERSION="${VERSION:-$DEFAULT_VERSION}"

# Validate version format (must be X.Y or vX.Y)
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+$ ]]; then
  echo "Error: Version must be in format X.Y."
  exit 1
fi

# Find README (assume it's named README.md)
README_FILE="/home/debian/KubernetesSubmissions/README.md"
if [[ ! -f "$README_FILE" ]]; then
  echo "Error: $README_FILE not found in current directory."
  exit 1
fi

# Compute relative path from README to current directory
RELATIVE_PATH=$(realpath --relative-to="$(dirname "$README_FILE")" "$PWD")
if [[ "$RELATIVE_PATH" == "." ]]; then
  RELATIVE_PATH=""
fi

# Construct the link (omit trailing slash if RELATIVE_PATH is empty)
if [[ -n "$RELATIVE_PATH" ]]; then
  LINK="- [$VERSION](https://github.com/Ik-12/KubernetesSubmissions/tree/$VERSION/$RELATIVE_PATH)"
else
  LINK="- [$VERSION](https://github.com/Ik-12/KubernetesSubmissions/tree/$VERSION)"
fi

# Clean up trailing blank lines in README
# Remove all empty lines at the end of the file
sed -i '${/^$/d;}' "$README_FILE"
while [[ -z $(tail -n1 "$README_FILE") ]]; do
  sed -i '${/^$/d;}' "$README_FILE"
done

# Append new link
echo "$LINK" >> "$README_FILE"

# Open README in vi for manual review
vi "$README_FILE"

# Commit and push
git add "$README_FILE"
git commit -m "Update README for $VERSION"
git push

# Create GitHub release
gh release create "$VERSION" --title "$VERSION" --notes "Release exercise $VERSION"

# Pull the release tag just created
git pull

echo "✅ Release $VERSION created and pushed successfully."
