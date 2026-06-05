import cv2
import numpy as np
import re
import os
import subprocess
import sys


class OCREngine:
    """Crash-safe OCR engine with Tesseract primary, EasyOCR/PaddleOCR optional."""

    def __init__(self):
        self.paddle_ocr = None
        self.easy_ocr = None
        self.tesseract_available = False
        self._easyocr_safe = False
        self._init_engines()

    def _init_engines(self):
        try:
            import pytesseract
            version = pytesseract.get_tesseract_version()
            self.tesseract_available = True
            print(f"[OCR] Tesseract available (v{version})")
        except Exception as e:
            print(f"[OCR] Tesseract not available: {e}")

        self._test_easyocr_safety()

        try:
            from paddleocr import PaddleOCR
            self.paddle_ocr = PaddleOCR(
                use_angle_cls=True, lang='en', use_gpu=False, show_log=False
            )
            print("[OCR] PaddleOCR initialized")
        except Exception as e:
            print(f"[OCR] PaddleOCR not available: {e}")

    def _test_easyocr_safety(self):
        try:
            result = subprocess.run(
                [sys.executable, '-c', 'import easyocr; print("EASYOK")'],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0 and "EASYOK" in result.stdout:
                self._easyocr_safe = True
                print("[OCR] EasyOCR import test passed")
            else:
                err = result.stderr[:300] if result.stderr else "unknown"
                print(f"[OCR] EasyOCR import test failed: {err}")
        except Exception as e:
            print(f"[OCR] EasyOCR safety test error: {e}")

    def _ensure_easyocr(self):
        if self.easy_ocr is not None:
            return
        if not self._easyocr_safe:
            return
        try:
            import easyocr
            self.easy_ocr = easyocr.Reader(
                ['en', 'hi', 'kn'], gpu=False, verbose=False
            )
            print("[OCR] EasyOCR initialized on demand")
        except Exception as e:
            print(f"[OCR] EasyOCR on-demand init failed: {e}")

    def preprocess_image(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not read image file")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)

        binary = cv2.adaptiveThreshold(
            enhanced, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        kernel = np.array([[-1, -1, -1],
                           [-1,  9, -1],
                           [-1, -1, -1]])
        sharpened = cv2.filter2D(binary, -1, kernel)

        preprocessed_path = image_path.replace('.', '_preprocessed.')
        cv2.imwrite(preprocessed_path, sharpened)
        return preprocessed_path, img

    def detect_language(self, text):
        if not text or not text.strip():
            return 'English'

        hindi_count = len(re.findall(r'[\u0900-\u097F]', text))
        kannada_count = len(re.findall(r'[\u0C80-\u0CFF]', text))
        total_chars = len(re.sub(r'\s', '', text))

        if total_chars == 0:
            return 'English'

        if kannada_count / total_chars > 0.05:
            return 'Kannada'
        if hindi_count / total_chars > 0.05:
            return 'Hindi'
        return 'English'

    def process_with_tesseract(self, image_path):
        if not self.tesseract_available:
            return None, 0
        try:
            import pytesseract
            custom_config = r'--oem 3 --psm 6'

            try:
                text = pytesseract.image_to_string(
                    image_path, lang='eng+hin+kan', config=custom_config
                )
                data = pytesseract.image_to_data(
                    image_path, lang='eng+hin+kan', config=custom_config,
                    output_type=pytesseract.Output.DICT
                )
            except Exception:
                text = pytesseract.image_to_string(
                    image_path, lang='eng', config=custom_config
                )
                data = pytesseract.image_to_data(
                    image_path, lang='eng', config=custom_config,
                    output_type=pytesseract.Output.DICT
                )

            confidences = [int(c) for c in data['conf'] if int(c) > 0]
            avg_conf = sum(confidences) / len(confidences) / 100 if confidences else 0.5
            return text.strip(), avg_conf
        except Exception as e:
            print(f"[OCR] Tesseract error: {e}")
            return None, 0

    def process_with_easyocr(self, image_path):
        self._ensure_easyocr()
        if self.easy_ocr is None:
            return None, 0
        try:
            result = self.easy_ocr.readtext(image_path)
            if not result:
                return None, 0
            texts = [d[1] for d in result]
            confidences = [d[2] for d in result]
            full_text = '\n'.join(texts)
            avg_conf = sum(confidences) / len(confidences) if confidences else 0
            return full_text, avg_conf
        except Exception as e:
            print(f"[OCR] EasyOCR error: {e}")
            return None, 0

    def process_with_paddle(self, image_path):
        if self.paddle_ocr is None:
            return None, 0
        try:
            result = self.paddle_ocr.ocr(image_path, cls=True)
            if not result or not result[0]:
                return None, 0
            texts = []
            confidences = []
            for line in result[0]:
                if line:
                    texts.append(line[1][0])
                    confidences.append(line[1][1])
            full_text = '\n'.join(texts)
            avg_conf = sum(confidences) / len(confidences) if confidences else 0
            return full_text, avg_conf
        except Exception as e:
            print(f"[OCR] PaddleOCR error: {e}")
            return None, 0

    def process_image(self, image_path):
        preprocessed_path, _ = self.preprocess_image(image_path)

        results = []

        tess_text, tess_conf = self.process_with_tesseract(preprocessed_path)
        if tess_text:
            results.append((tess_text, tess_conf, 'Tesseract (preprocessed)'))

        easy_text, easy_conf = self.process_with_easyocr(preprocessed_path)
        if easy_text:
            results.append((easy_text, easy_conf, 'EasyOCR (preprocessed)'))

        paddle_text, paddle_conf = self.process_with_paddle(preprocessed_path)
        if paddle_text:
            results.append((paddle_text, paddle_conf, 'PaddleOCR (preprocessed)'))

        tess_text_o, tess_conf_o = self.process_with_tesseract(image_path)
        if tess_text_o:
            results.append((tess_text_o, tess_conf_o, 'Tesseract (original)'))

        easy_text_o, easy_conf_o = self.process_with_easyocr(image_path)
        if easy_text_o:
            results.append((easy_text_o, easy_conf_o, 'EasyOCR (original)'))

        paddle_text_o, paddle_conf_o = self.process_with_paddle(image_path)
        if paddle_text_o:
            results.append((paddle_text_o, paddle_conf_o, 'PaddleOCR (original)'))

        if not results:
            return {
                'text': '',
                'confidence': 0.0,
                'language': 'English',
                'engine': 'No OCR engine available',
                'characters': 0,
                'words': 0,
                'preprocessed': True
            }

        results.sort(key=lambda x: x[1], reverse=True)
        best_text, best_conf, engine_used = results[0]

        language = self.detect_language(best_text)
        char_count = len(best_text)
        word_count = len(best_text.split()) if best_text else 0

        try:
            if os.path.exists(preprocessed_path):
                os.remove(preprocessed_path)
        except Exception:
            pass

        return {
            'text': best_text,
            'confidence': round(best_conf * 100, 2),
            'language': language,
            'engine': engine_used,
            'characters': char_count,
            'words': word_count,
            'preprocessed': True
        }
