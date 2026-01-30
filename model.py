def ml_classify_user(sip, years, goal):
    if years >= 10 and sip >= 5000:
        return "High Risk"
    elif years >= 5:
        return "Medium Risk"
    else:
        return "Low Risk"
