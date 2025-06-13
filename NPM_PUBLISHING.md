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
- [ ] Update version in `package.json` (currently `0.1.0-beta.1`)
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
npm install -g ./visidata-mcp-0.1.0-beta.1.tgz

# Test the command
visidata-mcp --help

# Run tests
npm test

# Cleanup
npm uninstall -g visidata-mcp
```

### 3. Publish Beta Version

```bash
# Publish to the beta tag
npm publish --tag beta

# Or if this is the first time
npm publish --access public --tag beta
```

### 4. Verify Publication

```bash
# Check if published
npm view visidata-mcp

# Install and test from npm
npm install -g visidata-mcp@beta
visidata-mcp --help
npm test
```

## Version Management

### Beta Versions
- Use format: `0.1.0-beta.1`, `0.1.0-beta.2`, etc.
- Publish with `--tag beta`
- Users install with `npm install -g visidata-mcp@beta`

### Stable Versions
- Use format: `0.1.0`, `0.2.0`, etc.
- Publish with `npm publish` (no tag = latest)
- Users install with `npm install -g visidata-mcp`

### Updating Versions

```bash
# For beta
npm version prerelease --preid=beta
# This changes 0.1.0-beta.1 → 0.1.0-beta.2

# For stable release
npm version patch  # 0.1.0 → 0.1.1
npm version minor  # 0.1.0 → 0.2.0
npm version major  # 0.1.0 → 1.0.0
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
npm install -g visidata-mcp@beta

# Ubuntu/Linux
sudo npm install -g visidata-mcp@beta

# Windows (PowerShell as Administrator)
npm install -g visidata-mcp@beta
```

### 3. Promote Beta to Stable

When ready to promote beta to stable:

```bash
# Add latest tag to the beta version
npm dist-tag add visidata-mcp@0.1.0-beta.1 latest

# Or publish a new stable version
npm version 0.1.0  # Remove -beta.1
npm publish
```

## Troubleshooting

### Permission Errors
```bash
# If you get permission errors
npm config set prefix '~/.local'
# Then add ~/.local/bin to PATH
```

### Package Already Exists
```bash
# If package name is taken, you might need to scope it
npm init --scope=@yourusername
# Then package becomes @yourusername/visidata-mcp
```

### Testing Different Node Versions
```bash
# Use nvm to test different Node versions
nvm use 14
npm test
nvm use 16
npm test
nvm use 18
npm test
```

## Commands Summary

```bash
# Complete publish workflow
npm login
npm test
npm pack && tar -tzf visidata-mcp-*.tgz  # inspect contents
npm publish --tag beta
npm view visidata-mcp
npm install -g visidata-mcp@beta && npm test
```

## Notes

- The npm package is a wrapper around the Python package
- It automatically installs the Python dependencies
- Users only need `npm install -g visidata-mcp@beta` to get started
- The package works on macOS, Linux, and Windows
- Python 3.8+ is still required but the npm package checks and guides users 