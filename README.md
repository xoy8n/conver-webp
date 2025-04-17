# WebP Converter MCP Server

A Model Context Protocol (MCP) server that converts PNG, JPG, and JPEG images to WebP format.

## Features

- Converts single images to WebP format
- Batch conversion of multiple images
- Converts base64 encoded images to WebP
- Option to keep or delete original files
- Adjustable quality and lossless settings

## Tools

### 1. Convert a Single Image to WebP

```typescript
mcp_conver_webp_convert_to_webp({
  image_path: string,       // Required: Path to the image file
  quality?: number,         // Optional: WebP quality (1-100), default: 80
  lossless?: boolean,       // Optional: Use lossless compression, default: false
  keep_original?: boolean,  // Optional: Keep original image, default: false
  output_dir?: string       // Optional: Output directory, default: same as input
})
```

### 2. Batch Convert Images to WebP

```typescript
mcp_conver_webp_batch_convert_to_webp({
  image_paths: string[],    // Required: Array of image paths
  quality?: number,         // Optional: WebP quality (1-100), default: 80
  lossless?: boolean,       // Optional: Use lossless compression, default: false
  keep_original?: boolean,  // Optional: Keep original images, default: false
  output_dir?: string       // Optional: Output directory, default: same as input
})
```

### 3. Convert Base64 Image to WebP

```typescript
mcp_conver_webp_convert_base64_to_webp({
  base64_image: string,     // Required: Base64 encoded image data
  output_path: string,      // Required: Output file path
  quality?: number,         // Optional: WebP quality (1-100), default: 80
  lossless?: boolean        // Optional: Use lossless compression, default: false
})
```

## Local Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the server:
   ```
   python server.py
   ```

## Hosting on Smithery

This MCP server is configured for deployment on Smithery using the included `Dockerfile` and `smithery.yaml` files.

## Testing

You can test the server using the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector python server.py
```
