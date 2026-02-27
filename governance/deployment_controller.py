def deployment_decision(risk_score):

    if risk_score > 0.75:
        return "BLOCK"
    elif risk_score > 0.4:
        return "MANUAL REVIEW"
    else:
        return "DEPLOY"