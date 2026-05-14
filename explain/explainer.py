def explain_decision(decision):
    ip = decision.get("src_ip")
    reason = decision.get("reason", "unknown")
    confidence = decision.get("confidence", 0)
    details = decision.get("details", {})
    ports = details.get("unique_ports", "?")
    conns = details.get("connection_count", "?")
    window = details.get("time_window", "60 seconds")
    print("\n[WHY THIS ALERT?]")
    if reason == "reconnaissance_detected":
        print(f"{ip} contacted {ports} different ports within {window}.")
        print("Rapid multi-port probing is a classic network reconnaissance pattern.")
    elif reason == "ssh_brute_force":
        print(f"{ip} made {conns} SSH attempts (port 22) within {window}.")
        print("High-frequency SSH attempts indicate a credential brute-force attack.")
        print("Recommendation: block IP and check auth.log for successful logins.")
    elif reason == "lateral_movement":
        print(f"{ip} hit port 445 (SMB) across multiple internal hosts within {window}.")
        print("SMB sweeping across a subnet is a classic lateral movement pattern.")
        print("Recommendation: isolate the source host and audit shared folder access.")
    elif reason == "c2_beacon":
        print(f"{ip} made {conns} outbound HTTPS connections at near-regular intervals.")
        print("Periodic beaconing to a fixed external IP is a strong indicator of C2 malware.")
        print("Recommendation: capture traffic for payload analysis and block destination.")
    elif reason == "dns_exfiltration":
        print(f"{ip} queried {ports} different DNS resolvers within {window}.")
        print("Querying many DNS servers rapidly is a known data exfiltration technique.")
        print("Recommendation: restrict DNS to internal resolvers only.")
    elif reason == "rdp_smb_chain":
        print(f"{ip} probed RDP (3389) then SMB/RPC (445/135) in sequence.")
        print("RDP followed by SMB is a textbook Windows lateral movement pattern.")
        print("Recommendation: disable RDP if unused and enforce NLA.")
    elif reason == "web_fuzzing":
        print(f"{ip} sent {conns} requests across HTTP ports within {window}.")
        print("Rapid HTTP requests across non-standard ports indicate web fuzzing.")
        print("Recommendation: enable WAF rules and review web server logs.")
    elif reason == "deprecated_protocol_sweep":
        print(f"{ip} used deprecated protocols (FTP/Telnet/SMTP/rsh) within {window}.")
        print("Legacy protocol use may indicate credential harvesting activity.")
        print("Recommendation: disable FTP, Telnet, rsh — use SFTP/SSH instead.")
    else:
        print(f"{ip} showed anomalous behaviour ({reason}) — {conns} connections, {ports} ports.")
        print("Manual investigation recommended.")
    print(f"Confidence: {confidence:.2f}")