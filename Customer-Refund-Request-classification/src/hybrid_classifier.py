from ML.predictor import predict_request_type
from gemini_classifier import classify_email_With_LLM_Model

CONFIDENCE_THRESHOLD = 0.90


def classify_email(from_addr, subject, body):


    print(f"Classifying email from hybridClassfier: {subject} — {from_addr}")

    email_text = f"""
    Subject: {subject}
    Body: {body}
    """


    ml_result = predict_request_type(
        email_text
    )


    if ml_result["confidence"] >= CONFIDENCE_THRESHOLD:

        print(f"Classified email: {subject} — {from_addr} using ML with confidence {ml_result['confidence']:.2f}")

        return {
            "request_type": ml_result["request_type"],
            "urgency": "medium",
            "one_line_summary": "Classified using ML",
            "suggested_action": "flag_for_review",
            "chargeback_risk": False,
            "confidence": ml_result["confidence"],
            "source": "ML"
        }


    else:

        print(f"Classified email: {subject} — {from_addr} using LLM with confidence {ml_result['confidence']:.2f}")

        result = classify_email_With_LLM_Model(
            from_addr,
            subject,
            body
        )

        result["confidence"] = ml_result["confidence"]
        result["source"] = "Gemini"

        return result
    