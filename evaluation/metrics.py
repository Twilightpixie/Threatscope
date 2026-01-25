def compute_metrics(decisions, ground_truth):
    tp = fp = fn = tn = 0

    for d in decisions:
        ip = d["src_ip"]
        predicted_malicious = d["action"] == "block"
        actual_malicious = ground_truth.get(ip, False)

        if predicted_malicious and actual_malicious:
            tp += 1
        elif predicted_malicious and not actual_malicious:
            fp += 1
        elif not predicted_malicious and actual_malicious:
            fn += 1
        elif not predicted_malicious and not actual_malicious:
            tn += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    return {
        "TP": tp,
        "FP": fp,
        "FN": fn,
        "TN": tn,
        "precision": precision,
        "recall": recall
    }
