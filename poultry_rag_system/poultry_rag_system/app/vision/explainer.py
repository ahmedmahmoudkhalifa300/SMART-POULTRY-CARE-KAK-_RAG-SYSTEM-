"""
Bridges the vision pipeline's disease prediction into the RAG pipeline to
produce a full, grounded explanation (symptoms/causes/treatment/prevention).
"""

import json
import re

from app.core.logger import get_logger
from app.rag.pipeline import RAGPipeline
from app.vision.predictor import DiagnosisPrediction, Predictor

logger = get_logger(__name__)

DISEASE_NAME_AR = {
    "Coccidiosis": "الكوكسيديا",
    "Healthy": "صحي",
    "New Castle Disease": "مرض نيوكاسل",
    "Salmonella": "السلمونيلا",
}


class DiagnosisExplainer:
    def __init__(self, predictor: Predictor | None = None, rag_pipeline: RAGPipeline | None = None):
        self.predictor = predictor or Predictor()
        self.rag_pipeline = rag_pipeline or RAGPipeline()

    def diagnose_and_explain(self, file_bytes: bytes) -> dict:
        prediction = self.predictor.predict(file_bytes)

        confidence = prediction.confidence
        if confidence < 0.4:
            explanation_text = (
                f"تنبيه: ثقة النموذج منخفضة ({confidence:.0%}). "
                "النتيجة قد لا تكون دقيقة. يرجى استشارة طبيب بيطري."
            )
            return {
                "disease": prediction.disease,
                "confidence": confidence,
                "explanation": explanation_text,
                "sources": [],
                "all_probabilities": prediction.all_probabilities,
            }

        rag_result = self.rag_pipeline.explain_diagnosis(
            prediction.disease, confidence
        )

        arabic_explanation = self._build_arabic_explanation(
            prediction.disease,
            confidence,
            rag_result.get("explanation", ""),
            rag_result.get("sources", []),
        )

        return {
            "disease": prediction.disease,
            "confidence": confidence,
            "explanation": arabic_explanation,
            "sources": rag_result.get("sources", []),
            "all_probabilities": prediction.all_probabilities,
        }

    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean markdown artifacts only, keep exact section headers and bullet structure."""
        text = re.sub(r'```(?:json)?\s*', '', text)
        text = text.replace('```', '')
        text = text.replace("**", "")
        text = re.sub(r'^- - ', '- ', text, flags=re.MULTILINE)
        lines = text.split('\n')
        normalized = []
        for line in lines:
            stripped = line.strip()
            if stripped:
                normalized.append(stripped)
        return '\n'.join(normalized)

    @staticmethod
    def _to_bullets(text: str) -> str:
        """Convert plain text into bullet points."""
        parts = [p.strip() for p in text.split('\n') if p.strip()]
        bullets = []
        for part in parts:
            sentences = [s.strip() for s in part.split('.') if s.strip()]
            for sentence in sentences:
                if sentence:
                    bullets.append(f"- {sentence}")
        return '\n'.join(bullets)

    @staticmethod
    def _build_arabic_explanation(disease_name: str, confidence: float, rag_answer: str, sources: list[dict]) -> str:
        rag_answer = (rag_answer or "").strip()

        prefixes = [
            "العلاج (من قاعدة المعرفة):",
            "العلاج:",
            "التشخيص:",
            "التشخيص الأولي:",
            "تشخيص أولي:",
            "تشخيص المرض:",
        ]
        for prefix in prefixes:
            if rag_answer.startswith(prefix):
                rag_answer = rag_answer[len(prefix):].strip()

        translated_disease = DISEASE_NAME_AR.get(disease_name, disease_name)

        # HEALTHY PATH: short format only
        if disease_name == "Healthy":
            return (
                f"🐔 تشخيص المرض: {translated_disease} بثقة {confidence:.0%}.\n"
                f"⚠️ يُرجى تأكيد التشخيص بواسطة طبيب بيطري."
            )

        # DISEASE PATH: full format
        fields = {}
        json_parsed = False
        try:
            start = rag_answer.find('{')
            end = rag_answer.rfind('}')
            if start != -1 and end != -1 and end > start:
                json_str = rag_answer[start:end + 1]
                fields = json.loads(json_str)
                json_parsed = True
        except Exception:
            pass

        causes_text = fields.get("causes", "").strip()
        symptoms_text = fields.get("symptoms", "").strip()
        treatment_text = fields.get("treatment", "").strip()
        prevention_text = fields.get("prevention", "").strip()

        if not json_parsed or (not causes_text and not symptoms_text and not treatment_text and not prevention_text):
            clean_rag = rag_answer.replace("**", "")
            clean_rag = re.sub(r'```(?:json)?\s*', '', clean_rag)
            clean_rag = clean_rag.replace('```', '')

            paragraphs = [p.strip() for p in clean_rag.split('\n\n') if p.strip()]
            for para in paragraphs:
                para_lower = para.lower()
                if any(word in para_lower for word in ['علاج', 'يستخدم', 'تولترازوريل', 'سلفا', 'أمبروليوم', 'مغلي', 'شيح', 'كركم', 'دواء', 'مدة']):
                    treatment_text += ('\n' if treatment_text else '') + para
                elif any(word in para_lower for word in ['سبب', 'تسبب', 'طفيليات', 'عدوى', 'تنتقل', 'بيض', 'تلوث']):
                    causes_text += ('\n' if causes_text else '') + para
                elif any(word in para_lower for word in ['وقاية', 'نظافة', 'تعقيم', 'عزل', 'تجنب', 'تحسين', 'اكتظاظ']):
                    prevention_text += ('\n' if prevention_text else '') + para
                elif any(word in para_lower for word in ['أعراض', 'إسهال', 'كششان', 'شحوب', 'فقر الدم', 'تراجع', 'شهية']):
                    symptoms_text += ('\n' if symptoms_text else '') + para

        lines = []
        lines.append(f"🐔 تشخيص المرض: {translated_disease} بثقة {confidence:.0%}.")
        lines.append(f"⚠️ يُرجى تأكيد التشخيص بواسطة طبيب بيطري.")

        if causes_text:
            lines.append("")
            lines.append("🦠 الأسباب:")
            lines.append(DiagnosisExplainer._to_bullets(causes_text))

        if symptoms_text:
            lines.append("")
            lines.append("🔍 الأعراض:")
            lines.append(DiagnosisExplainer._to_bullets(symptoms_text))

        if treatment_text:
            lines.append("")
            lines.append("💊 العلاج:")
            lines.append(DiagnosisExplainer._to_bullets(treatment_text))

        if prevention_text:
            lines.append("")
            lines.append("🛡️ الوقاية:")
            lines.append(DiagnosisExplainer._to_bullets(prevention_text))

        lines.append("")
        lines.append("📌 ملاحظة:")
        lines.append("النتيجة دي معمولة بالذكاء الاصطناعي بهدف المساعدة، لكنها ما تغنيش عن تشخيص الطبيب البيطري.")

        result = '\n'.join(lines)
        return DiagnosisExplainer._clean_text(result)
