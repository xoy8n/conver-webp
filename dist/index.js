"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const mcp_js_1 = require("@modelcontextprotocol/sdk/server/mcp.js");
const stdio_js_1 = require("@modelcontextprotocol/sdk/server/stdio.js");
const zod_1 = require("zod");
const convert_1 = require("./convert");
// 서버 초기화
const server = new mcp_js_1.McpServer({
    name: "WebP Converter",
    version: "1.0.0",
});
// 도구 정의
server.tool("convert_to_webp", {
    image_path: zod_1.z.string(),
    quality: zod_1.z.number().default(80),
    lossless: zod_1.z.boolean().default(false),
    output_dir: zod_1.z.string().nullable().default(null),
    keep_original: zod_1.z.boolean().default(false),
}, async (params) => {
    const result = await (0, convert_1.convertToWebP)(params.image_path, params.quality, params.lossless, params.output_dir, params.keep_original);
    return {
        content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
    };
});
server.tool("batch_convert_to_webp", {
    image_paths: zod_1.z.array(zod_1.z.string()),
    quality: zod_1.z.number().default(80),
    lossless: zod_1.z.boolean().default(false),
    output_dir: zod_1.z.string().nullable().default(null),
    keep_original: zod_1.z.boolean().default(false),
}, async (params) => {
    const results = [];
    for (const imagePath of params.image_paths) {
        const result = await (0, convert_1.convertToWebP)(imagePath, params.quality, params.lossless, params.output_dir, params.keep_original);
        results.push(result);
    }
    return {
        content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
    };
});
server.tool("convert_base64_to_webp", {
    base64_image: zod_1.z.string(),
    output_path: zod_1.z.string(),
    quality: zod_1.z.number().default(80),
    lossless: zod_1.z.boolean().default(false),
}, async (params) => {
    const { convertBase64ToWebP } = await Promise.resolve().then(() => __importStar(require("./convert")));
    const result = await convertBase64ToWebP(params.base64_image, params.output_path, params.quality, params.lossless);
    return {
        content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
    };
});
// 서버 시작
const transport = new stdio_js_1.StdioServerTransport();
server.connect(transport).catch((error) => {
    console.error("서버 연결 오류:", error);
    process.exit(1);
});
