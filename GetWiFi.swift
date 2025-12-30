import Foundation
import CoreWLAN
import CoreLocation

class WiFiReader: NSObject, CLLocationManagerDelegate {
    let locationManager = CLLocationManager()
    let wifiClient = CWWiFiClient.shared()

    override init() {
        super.init()
        locationManager.delegate = self
    }

    func start() {
        // Trigger the permission request
        locationManager.requestAlwaysAuthorization()
        checkWiFi()
    }

    func checkWiFi() {
        if let interface = wifiClient.interface() {
            if let name = interface.ssid() {
                print(name)
                exit(0)
            }
        }
    }

    func locationManager(_ manager: CLLocationManager, didChangeAuthorization status: CLAuthorizationStatus) {
        // On macOS, we only check for .authorizedAlways
        if status == .authorizedAlways {
            checkWiFi()
        } else if status == .denied {
            print("PERMISSION DENIED. Go to System Settings > Privacy > Location Services > Terminal.")
            exit(1)
        } else if status.rawValue == 0 {
            // Status 0 is .notDetermined. We wait for the user to click Allow.
            print("Waiting for permission...")
        }
    }
}

let reader = WiFiReader()
reader.start()
RunLoop.main.run()
