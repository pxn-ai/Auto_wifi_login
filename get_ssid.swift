//
//  get_ssid.swift
//  
//
//  Created by Pasan Kaluarachchi on 2025-12-29.
//

import CoreWLAN

// Get the default Wi-Fi interface
if let interface = CWWiFiClient.shared().interface() {
    // Try to get the SSID
    if let ssid = interface.ssid() {
        print(ssid)
    } else {
        // Connected to hardware, but no network name found
        print("None")
    }
} else {
    // No Wi-Fi interface found
    print("No Interface")
}
