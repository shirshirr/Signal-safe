import numpy as np

def shap_explain(model, X):
    try:
        import shap
    except Exception as e:
        raise RuntimeError("shap not installed. Run: pip install shap matplotlib")
    explainer = shap.KernelExplainer(lambda x: model.predict(x), shap.sample(X, min(50, len(X))))
    return explainer.shap_values(X[:min(10, len(X))])
