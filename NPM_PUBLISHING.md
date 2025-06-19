# NPM Publishing Guide for visidata-mcp

This guide explains how to publish the visidata-mcp npm package.

## Prerequisites

1. **npm account**: Create an account at [npmjs.com](https://www.npmjs.com)
2. **npm CLI**: Ensure you have npm installed and are logged in:
   ```bash
   npm login
   ```

## Publishing Process

### 1. Pre-publish Checklist

- [ ] Ensure Python package is published to PyPI first
- [ ] Update version in `package.json` (currently `0.1.7`)
- [ ] Test the package locally
- [ ] Update README.md if needed
- [ ] Ensure all scripts have proper permissions

### 2. Test Locally

Before publishing, test the package locally:

```bash
# Test the package structure
npm pack
# This creates a .tgz file you can inspect

# Test installation locally
npm install -g ./moeloubani-visidata-mcp-0.1.6.tgz

# Test the command
visidata-mcp --help

# Run tests
npm test

# Cleanup
npm uninstall -g @moeloubani/visidata-mcp
```

### 3. Publish Version

```bash
# Publish to the beta tag (for testing)
npm publish --tag beta

# Or publish as latest (for stable release)
npm publish
```

### 4. Verify Publication

```bash
# Check if published
npm view @moeloubani/visidata-mcp

# Install and test from npm
npm install -g @moeloubani/visidata-mcp@beta
visidata-mcp --help
```

## Version Management

### Beta Versions
- Use format: `0.1.6-beta.1`, `0.1.6-beta.2`, etc.
- Publish with `--tag beta`
- Users install with `npm install -g @moeloubani/visidata-mcp@beta`

### Stable Versions
- Use format: `0.1.6`, `0.2.0`, etc.
- Publish with `npm publish` (no tag = latest)
- Users install with `npm install -g @moeloubani/visidata-mcp`

### Updating Versions

```bash
# For beta
npm version prerelease --preid=beta
# This changes 0.1.6 → 0.1.7-beta.1

# For stable release
npm version patch  # 0.1.6 → 0.1.7
npm version minor  # 0.1.6 → 0.2.0
npm version major  # 0.1.6 → 1.0.0
```

## Post-Publication

### 1. Update Documentation

- Update README.md with the new version
- Update any installation instructions
- Create release notes

### 2. Test Installation

Test on different platforms:

```bash
# macOS
npm install -g @moeloubani/visidata-mcp

# Ubuntu/Linux
sudo npm install -g @moeloubani/visidata-mcp

# Windows (PowerShell as Administrator)
npm install -g @moeloubani/visidata-mcp
```

### 3. Promote Beta to Stable

When ready to promote beta to stable:

```bash
# Add latest tag to the beta version
npm dist-tag add @moeloubani/visidata-mcp@0.1.6-beta.1 latest

# Or publish a new stable version
npm version 0.1.6  # Remove -beta.1
npm publish
```

## Commands Summary

```bash
# Complete publish workflow
npm login
npm test
npm pack && tar -tzf moeloubani-visidata-mcp-*.tgz  # inspect contents
npm publish --tag beta
npm view @moeloubani/visidata-mcp
npm install -g @moeloubani/visidata-mcp@beta
```

## Notes

- The npm package is a wrapper around the Python package
- It automatically installs the Python dependencies including matplotlib, seaborn, scipy
- Users only need `npm install -g @moeloubani/visidata-mcp` to get started
- The package works on macOS, Linux, and Windows
- Python 3.10+ is required and the npm package checks and guides users 