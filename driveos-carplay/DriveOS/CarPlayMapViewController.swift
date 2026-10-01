import UIKit
import MapKit

final class CarPlayMapViewController: UIViewController, MKMapViewDelegate {
    let mapView = MKMapView()

    override func viewDidLoad() {
        super.viewDidLoad()

        mapView.frame = view.bounds
        mapView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        mapView.delegate = self
        mapView.showsUserLocation = true
        mapView.showsCompass = false
        mapView.showsScale = false
        mapView.pointOfInterestFilter = .excludingAll
        mapView.preferredConfiguration = MKStandardMapConfiguration(
            elevationStyle: .realistic,
            emphasisStyle: .muted
        )
        view.addSubview(mapView)
    }

    func recenter(on coordinate: CLLocationCoordinate2D, heading: CLLocationDirection = 0) {
        let camera = MKMapCamera(
            lookingAtCenter: coordinate,
            fromDistance: 850,
            pitch: 58,
            heading: heading >= 0 ? heading : 0
        )
        mapView.setCamera(camera, animated: true)
    }

    func display(route: MKRoute) {
        mapView.removeOverlays(mapView.overlays)
        mapView.addOverlay(route.polyline)
        mapView.setVisibleMapRect(
            route.polyline.boundingMapRect,
            edgePadding: UIEdgeInsets(top: 80, left: 70, bottom: 80, right: 70),
            animated: true
        )
    }

    func mapView(_ mapView: MKMapView, rendererFor overlay: MKOverlay) -> MKOverlayRenderer {
        guard let polyline = overlay as? MKPolyline else { return MKOverlayRenderer(overlay: overlay) }
        let renderer = MKPolylineRenderer(polyline: polyline)
        renderer.strokeColor = UIColor.systemCyan
        renderer.lineWidth = 8
        renderer.lineCap = .round
        renderer.lineJoin = .round
        return renderer
    }
}
