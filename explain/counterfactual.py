def print_counterfactual(decision):
    if decision["action"] != "block":
        return

    print("\nIf not blocked:")
    print("• Possible credential attack")
    print("• Possible lateral movement")
    print("• Estimated risk: HIGH")
