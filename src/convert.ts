import * as fs from "fs";
import * as path from "path";
import sharp from "sharp";

/**
 * 이미지 파일을 WebP 형식으로 변환합니다.
 */
export async function convertToWebP(
  imagePath: string,
  quality: number = 80,
  lossless: boolean = false,
  outputDir: string | null = null,
  keepOriginal: boolean = false
): Promise<any> {
  try {
    // 경로 정규화 - 플랫폼에 맞는 경로 구분자 사용
    const normalizedImagePath = imagePath.split("/").join(path.sep);

    // 절대 경로 유지
    const absoluteImagePath = path.isAbsolute(normalizedImagePath)
      ? normalizedImagePath
      : path.resolve(normalizedImagePath);

    console.log(`Attempting to process: ${absoluteImagePath}`);

    // 입력 파일이 존재하는지 확인
    if (!fs.existsSync(absoluteImagePath)) {
      throw new Error(`Input file is missing: ${absoluteImagePath}`);
    }

    // 이미지 확장자 확인
    const ext = path.extname(absoluteImagePath).toLowerCase();
    if (![".png", ".jpg", ".jpeg"].includes(ext)) {
      throw new Error(`지원되지 않는 이미지 형식입니다: ${ext}`);
    }

    // 출력 파일명 생성
    const filename = path.basename(absoluteImagePath, ext);
    const outputPath = outputDir
      ? path.join(outputDir, `${filename}.webp`)
      : path.join(path.dirname(absoluteImagePath), `${filename}.webp`);

    // 출력 디렉토리가 지정된 경우 존재하는지 확인하고 생성
    const outputDirPath = outputDir || path.dirname(outputPath);
    if (!fs.existsSync(outputDirPath)) {
      fs.mkdirSync(outputDirPath, { recursive: true });
    }

    // 변환 옵션 설정
    const options = { quality, lossless };

    console.log(`Converting to WebP: ${outputPath}`);

    // 이미지 변환
    await sharp(absoluteImagePath).webp(options).toFile(outputPath);

    // 원본 파일 삭제 여부 확인
    if (!keepOriginal) {
      fs.unlinkSync(absoluteImagePath);
    }

    // 결과 반환
    return {
      success: true,
      input_path: absoluteImagePath,
      output_path: outputPath,
      size_before: fs.statSync(keepOriginal ? absoluteImagePath : outputPath)
        .size,
      size_after: fs.statSync(outputPath).size,
      quality,
      lossless,
    };
  } catch (error: any) {
    console.error(`Error converting image: ${error.message}`);
    return {
      success: false,
      error: error.message,
      input_path: imagePath,
    };
  }
}

/**
 * Base64로 인코딩된 이미지를 WebP로 변환합니다.
 */
export async function convertBase64ToWebP(
  base64Image: string,
  outputPath: string,
  quality: number = 80,
  lossless: boolean = false
): Promise<any> {
  try {
    // 경로 정규화
    const normalizedOutputPath = outputPath.split("/").join(path.sep);

    // Base64 데이터에서 메타데이터 제거 (data:image/jpeg;base64, 등)
    const base64Data = base64Image.replace(/^data:image\/\w+;base64,/, "");
    const buffer = Buffer.from(base64Data, "base64");

    // 출력 디렉토리 확인 및 생성
    const absoluteOutputPath = path.isAbsolute(normalizedOutputPath)
      ? normalizedOutputPath
      : path.resolve(normalizedOutputPath);
    const outputDir = path.dirname(absoluteOutputPath);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    // 변환 옵션 설정
    const options = { quality, lossless };

    // 이미지 변환
    await sharp(buffer).webp(options).toFile(absoluteOutputPath);

    // 결과 반환
    return {
      success: true,
      output_path: absoluteOutputPath,
      size: fs.statSync(absoluteOutputPath).size,
      quality,
      lossless,
    };
  } catch (error: any) {
    console.error(`Error converting base64 image: ${error.message}`);
    return {
      success: false,
      error: error.message,
      output_path: outputPath,
    };
  }
}
