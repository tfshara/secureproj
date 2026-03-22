def deployment_decision(risk_score):

    if risk_score > 0.65:          # 🔥 lowered
        return "BLOCK"
    elif risk_score > 0.35:        # 🔥 slightly lowered
        return "MANUAL REVIEW"
    else:
        return "DEPLOY"