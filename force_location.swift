import CoreLocation

class LocationRequester: NSObject, CLLocationManagerDelegate {
    let manager = CLLocationManager()
    
    override init() {
        super.init()
        manager.delegate = self
        // Request permission
        manager.requestAlwaysAuthorization()
        // Trigger a location fetch to force the OS to notice us
        manager.startUpdatingLocation()
    }
    
    func locationManager(_ manager: CLLocationManager, didChangeAuthorization status: CLAuthorizationStatus) {
        let statusString = String(status.rawValue)
        
        if status.rawValue == 0 {
            print("Status: Not Determined (0). Waiting for popup...")
            // Do NOT exit. We are waiting for the user.
        } else {
            print("Status Updated: \(status.rawValue)")
            if status.rawValue == 3 || status.rawValue == 4 {
                print("SUCCESS: Permission Granted.")
                exit(0)
            } else if status.rawValue == 2 {
                print("FAILURE: Permission Denied.")
                exit(1)
            }
        }
    }
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        // If we got a location, we definitely have permission
        print("Location received! Permission confirmed.")
        exit(0)
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        // Ignore temporary errors while waiting
        // print("Waiting... (Error: \(error.localizedDescription))")
    }
}

print("Requesting Location Access...")
let requester = LocationRequester()
RunLoop.main.run()
