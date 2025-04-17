#!/usr/bin/env python3
import json
import os
import sys
import traceback
from PIL import Image
import uuid

# 디버그 모드 확인
DEBUG = os.environ.get("DEBUG", "0") == "1"

def log(message):
    """Log a message to stderr"""
    print(f"[LOG] {message}", file=sys.stderr, flush=True)

def debug(message):
    """Log a debug message to stderr if DEBUG is enabled"""
    if DEBUG:
        print(f"[DEBUG] {message}", file=sys.stderr, flush=True)

def send_response(response):
    """Send a response to stdout"""
    try:
        debug(f"Sending response: {json.dumps(response)[:200]}...")
        print(json.dumps(response), flush=True)
    except Exception as e:
        log(f"Error sending response: {str(e)}")

def receive_request():
    """Receive a request from stdin"""
    try:
        debug("Waiting for request...")
        line = sys.stdin.readline()
        if not line:
            log("Received empty line, returning None")
            return None
        debug(f"Received request: {line[:200]}...")
        return json.loads(line)
    except Exception as e:
        log(f"Error receiving request: {str(e)}")
        raise

def convert_to_webp(image_path, quality=80, lossless=False, keep_original=False):
    """Convert an image to WebP format and replace the original"""
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            return {"success": False, "error": f"File not found: {image_path}"}
        
        # Get file info
        directory, filename = os.path.split(image_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(directory, f"{name}.webp")
        
        # Only process supported formats
        if ext.lower() not in ['.png', '.jpg', '.jpeg']:
            return {"success": False, "error": f"Unsupported format: {ext}"}
        
        # Convert image to WebP
        img = Image.open(image_path)
        img.save(output_path, format="WEBP", quality=quality, lossless=lossless)
        
        # Delete original file if not keeping it
        if not keep_original:
            os.remove(image_path)
        
        return {"success": True, "output_path": output_path}
    
    except Exception as e:
        error_msg = f"Error converting {image_path}: {str(e)}"
        log(error_msg)
        return {"success": False, "error": error_msg}

def batch_convert_to_webp(image_paths, quality=80, lossless=False, keep_original=False, output_dir=None):
    """Convert multiple images to WebP format"""
    results = []
    
    for image_path in image_paths:
        # Determine output path
        if output_dir:
            directory, filename = os.path.split(image_path)
            name, ext = os.path.splitext(filename)
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{name}.webp")
        else:
            result = convert_to_webp(image_path, quality, lossless, keep_original)
            results.append(result)
            continue
        
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                results.append({"success": False, "error": f"File not found: {image_path}"})
                continue
            
            # Only process supported formats
            _, ext = os.path.splitext(image_path)
            if ext.lower() not in ['.png', '.jpg', '.jpeg']:
                results.append({"success": False, "error": f"Unsupported format: {ext}"})
                continue
            
            # Convert image to WebP
            img = Image.open(image_path)
            img.save(output_path, format="WEBP", quality=quality, lossless=lossless)
            
            # Delete original file if not keeping it
            if not keep_original:
                os.remove(image_path)
            
            results.append({"success": True, "output_path": output_path})
        
        except Exception as e:
            error_msg = f"Error converting {image_path}: {str(e)}"
            log(error_msg)
            results.append({"success": False, "error": error_msg})
    
    return results

def convert_base64_to_webp(base64_image, output_path, quality=80, lossless=False):
    """Convert a base64 encoded image to WebP format"""
    try:
        import base64
        from io import BytesIO
        
        # Decode base64 image
        if "," in base64_image:
            base64_image = base64_image.split(",", 1)[1]
        
        image_data = base64.b64decode(base64_image)
        img = Image.open(BytesIO(image_data))
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Save as WebP
        img.save(output_path, format="WEBP", quality=quality, lossless=lossless)
        
        return {"success": True, "output_path": output_path}
    
    except Exception as e:
        error_msg = f"Error converting base64 image: {str(e)}"
        log(error_msg)
        return {"success": False, "error": error_msg}

def handle_initialize():
    """Handle the initialize method"""
    return {
        "jsonrpc": "2.0",
        "result": {
            "name": "WebP Converter",
            "version": "1.0.0",
            "vendor": "MCP Tools",
            "capabilities": ["stdio", "mcp1"]
        }
    }

def handle_tools_list():
    """Handle the tools list method"""
    return {
        "jsonrpc": "2.0",
        "result": {
            "tools": [
                {
                    "name": "mcp_conver_webp_convert_to_webp",
                    "description": "Convert a single image to WebP format",
                    "schema": {
                        "$schema": "http://json-schema.org/draft-07/schema#",
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["image_path"],
                        "properties": {
                            "image_path": {
                                "type": "string"
                            },
                            "quality": {
                                "type": "number",
                                "default": 80
                            },
                            "lossless": {
                                "type": "boolean",
                                "default": False
                            },
                            "keep_original": {
                                "type": "boolean",
                                "default": False
                            },
                            "output_dir": {
                                "type": ["string", "null"],
                                "default": None
                            }
                        }
                    }
                },
                {
                    "name": "mcp_conver_webp_batch_convert_to_webp",
                    "description": "Convert multiple images to WebP format",
                    "schema": {
                        "$schema": "http://json-schema.org/draft-07/schema#",
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["image_paths"],
                        "properties": {
                            "image_paths": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "quality": {
                                "type": "number",
                                "default": 80
                            },
                            "lossless": {
                                "type": "boolean",
                                "default": False
                            },
                            "keep_original": {
                                "type": "boolean",
                                "default": False
                            },
                            "output_dir": {
                                "type": ["string", "null"],
                                "default": None
                            }
                        }
                    }
                },
                {
                    "name": "mcp_conver_webp_convert_base64_to_webp",
                    "description": "Convert a base64 encoded image to WebP format",
                    "schema": {
                        "$schema": "http://json-schema.org/draft-07/schema#",
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["base64_image", "output_path"],
                        "properties": {
                            "base64_image": {
                                "type": "string"
                            },
                            "output_path": {
                                "type": "string"
                            },
                            "quality": {
                                "type": "number",
                                "default": 80
                            },
                            "lossless": {
                                "type": "boolean",
                                "default": False
                            }
                        }
                    }
                }
            ]
        }
    }

def handle_health_check():
    """Handle the health check method"""
    return {
        "jsonrpc": "2.0",
        "result": {
            "status": "ok",
            "version": "1.0.0"
        }
    }

def handle_tool_call(request):
    """Handle a tool call request"""
    method = request.get("method")
    params = request.get("params", {})
    
    if method == "mcp_conver_webp_convert_to_webp":
        image_path = params.get("image_path")
        quality = params.get("quality", 80)
        lossless = params.get("lossless", False)
        keep_original = params.get("keep_original", False)
        output_dir = params.get("output_dir")
        
        if output_dir:
            directory, filename = os.path.split(image_path)
            name, ext = os.path.splitext(filename)
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{name}.webp")
            
            try:
                img = Image.open(image_path)
                img.save(output_path, format="WEBP", quality=quality, lossless=lossless)
                
                if not keep_original:
                    os.remove(image_path)
                
                result = {"success": True, "output_path": output_path}
            except Exception as e:
                result = {"success": False, "error": str(e)}
        else:
            result = convert_to_webp(image_path, quality, lossless, keep_original)
    
    elif method == "mcp_conver_webp_batch_convert_to_webp":
        image_paths = params.get("image_paths", [])
        quality = params.get("quality", 80)
        lossless = params.get("lossless", False)
        keep_original = params.get("keep_original", False)
        output_dir = params.get("output_dir")
        
        result = batch_convert_to_webp(image_paths, quality, lossless, keep_original, output_dir)
    
    elif method == "mcp_conver_webp_convert_base64_to_webp":
        base64_image = params.get("base64_image")
        output_path = params.get("output_path")
        quality = params.get("quality", 80)
        lossless = params.get("lossless", False)
        
        result = convert_base64_to_webp(base64_image, output_path, quality, lossless)
    
    else:
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            },
            "id": request.get("id")
        }
    
    return {
        "jsonrpc": "2.0",
        "result": result,
        "id": request.get("id")
    }

def main():
    """Main function to handle MCP requests"""
    log("Starting WebP Converter MCP server...")
    
    try:
        log("Checking Pillow installation...")
        pil_version = Image.__version__
        log(f"Pillow version: {pil_version}")
    except Exception as e:
        log(f"Error checking Pillow installation: {str(e)}")
    
    while True:
        try:
            request = receive_request()
            
            if request is None:
                log("Received None request, exiting...")
                break
            
            request_id = request.get("id", "unknown")
            method = request.get("method", "unknown")
            log(f"Processing request ID {request_id}, method: {method}")
            
            if method == "initialize":
                response = handle_initialize()
                log("Handled initialize request")
            elif method == "/tools/list":
                response = handle_tools_list()
                log("Handled tools list request")
            elif method == "/health":
                response = handle_health_check()
                log("Handled health check request")
            else:
                log(f"Handling tool call: {method}")
                response = handle_tool_call(request)
                log(f"Handled tool call: {method}")
            
            response["id"] = request.get("id")
            send_response(response)
        
        except Exception as e:
            error_message = f"Unhandled error: {str(e)}\n{traceback.format_exc()}"
            log(error_message)
            
            error_response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32000,
                    "message": "Internal error",
                    "data": {
                        "details": str(e)
                    }
                },
                "id": request.get("id") if request else None
            }
            
            send_response(error_response)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"Fatal error in main: {str(e)}\n{traceback.format_exc()}")
        sys.exit(1) 