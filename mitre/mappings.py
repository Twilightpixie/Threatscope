MITRE_RECON_MAPPING = {
    "reconnaissance_detected":  {"tactic":"Discovery","tactic_id":"TA0007","technique":"Network Service Discovery","technique_id":"T1046"},
    "ssh_brute_force":          {"tactic":"Credential Access","tactic_id":"TA0006","technique":"Brute Force: Password Spraying","technique_id":"T1110.003"},
    "lateral_movement":         {"tactic":"Lateral Movement","tactic_id":"TA0008","technique":"Remote Services: SMB","technique_id":"T1021.002"},
    "c2_beacon":                {"tactic":"Command and Control","tactic_id":"TA0011","technique":"Application Layer Protocol","technique_id":"T1071.001"},
    "dns_exfiltration":         {"tactic":"Exfiltration","tactic_id":"TA0010","technique":"Exfiltration Over DNS","technique_id":"T1048.003"},
    "rdp_smb_chain":            {"tactic":"Lateral Movement","tactic_id":"TA0008","technique":"Remote Desktop Protocol","technique_id":"T1021.001"},
    "web_fuzzing":              {"tactic":"Initial Access","tactic_id":"TA0001","technique":"Exploit Public-Facing Application","technique_id":"T1190"},
    "deprecated_protocol_sweep":{"tactic":"Discovery","tactic_id":"TA0007","technique":"Network Service Discovery","technique_id":"T1046"},
    "normal_behavior":          {"tactic":None,"tactic_id":None,"technique":None,"technique_id":None},
}