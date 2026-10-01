import UIKit
import CarPlay
import MapKit
import CoreLocation

final class CarPlaySceneDelegate: UIResponder,
                                  CPTemplateApplicationSceneDelegate,
                                  CPSearchTemplateDelegate,
                                  CPMapTemplateDelegate,
                                  CLLocationManagerDelegate {

    private var interfaceController: CPInterfaceController?
    private var carWindow: CPWindow?
    private var mapTemplate: CPMapTemplate?
    private var mapViewController: CarPlayMapViewController?

    private let locationManager = CLLocationManager()
    private var currentLocation: CLLocation?
    private var selectedDestination: MKMapItem?
    private var activeRoute: MKRoute?
    private var navigationSession: CPNavigationSession?

    func templateApplicationScene(
        _ templateApplicationScene: CPTemplateApplicationScene,
        didConnect interfaceController: CPInterfaceController,
        to window: CPWindow
    ) {
        self.interfaceController = interfaceController
        self.carWindow = window

        let mapVC = CarPlayMapViewController()
        mapViewController = mapVC
        window.rootViewController = mapVC

        let mapTemplate = makeMapTemplate()
        self.mapTemplate = mapTemplate
        interfaceController.setRootTemplate(mapTemplate, animated: false, completion: nil)

        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBestForNavigation
        locationManager.activityType = .automotiveNavigation
        locationManager.requestWhenInUseAuthorization()
        locationManager.startUpdatingLocation()
    }

    func templateApplicationScene(
        _ templateApplicationScene: CPTemplateApplicationScene,
        didDisconnect interfaceController: CPInterfaceController,
        from window: CPWindow
    ) {
        navigationSession?.cancelTrip()
        navigationSession = nil
        locationManager.stopUpdatingLocation()
        self.interfaceController = nil
        self.carWindow = nil
        self.mapTemplate = nil
        self.mapViewController = nil
    }

    private func makeMapTemplate() -> CPMapTemplate {
        let template = CPMapTemplate()
        template.mapDelegate = self

        let searchButton = CPMapButton { [weak self] _ in
            self?.showSearch()
        }
        searchButton.image = UIImage(systemName: "magnifyingglass")

        let recenterButton = CPMapButton { [weak self] _ in
            self?.recenter()
        }
        recenterButton.image = UIImage(systemName: "location.fill")

        template.mapButtons = [searchButton, recenterButton]
        return template
    }

    private func showSearch() {
        guard let interfaceController else { return }
        let search = CPSearchTemplate()
        search.delegate = self
        interfaceController.pushTemplate(search, animated: true, completion: nil)
    }

    private func recenter() {
        guard let location = currentLocation else { return }
        mapViewController?.recenter(
            on: location.coordinate,
            heading: location.course >= 0 ? location.course : 0
        )
    }

    func searchTemplate(
        _ searchTemplate: CPSearchTemplate,
        updatedSearchText searchText: String,
        completionHandler: @escaping ([CPListItem]) -> Void
    ) {
        let text = searchText.trimmingCharacters(in: .whitespacesAndNewlines)
        guard text.count >= 2 else {
            completionHandler([])
            return
        }

        let request = MKLocalSearch.Request()
        request.naturalLanguageQuery = text
        if let location = currentLocation {
            request.region = MKCoordinateRegion(
                center: location.coordinate,
                latitudinalMeters: 100_000,
                longitudinalMeters: 100_000
            )
        }

        MKLocalSearch(request: request).start { response, _ in
            let results = (response?.mapItems ?? []).prefix(8).map { mapItem -> CPListItem in
                let detail = [
                    mapItem.placemark.locality,
                    mapItem.placemark.administrativeArea
                ].compactMap { $0 }.joined(separator: ", ")

                let item = CPListItem(
                    text: mapItem.name ?? "Destination",
                    detailText: detail
                )
                item.userInfo = mapItem
                return item
            }
            completionHandler(Array(results))
        }
    }

    func searchTemplate(
        _ searchTemplate: CPSearchTemplate,
        selectedResult item: CPListItem,
        completionHandler: @escaping () -> Void
    ) {
        guard let destination = item.userInfo as? MKMapItem else {
            completionHandler()
            return
        }

        selectedDestination = destination
        interfaceController?.popTemplate(animated: true, completion: nil)
        buildRoute(to: destination)
        completionHandler()
    }

    private func buildRoute(to destination: MKMapItem) {
        let request = MKDirections.Request()

        if let location = currentLocation {
            let placemark = MKPlacemark(coordinate: location.coordinate)
            request.source = MKMapItem(placemark: placemark)
        } else {
            request.source = MKMapItem.forCurrentLocation()
        }

        request.destination = destination
        request.transportType = .automobile
        request.requestsAlternateRoutes = true

        MKDirections(request: request).calculate { [weak self] response, _ in
            guard let self,
                  let response,
                  let primary = response.routes.first,
                  let source = request.source else { return }

            self.activeRoute = primary
            self.mapViewController?.display(route: primary)

            let routes = Array(response.routes.prefix(3))
            let choices = routes.map { route -> CPRouteChoice in
                let choice = CPRouteChoice(
                    summaryVariants: [route.name.isEmpty ? "Recommended route" : route.name],
                    additionalInformationVariants: [self.durationText(route.expectedTravelTime)],
                    selectionSummaryVariants: [self.distanceText(route.distance)]
                )
                choice.userInfo = route
                return choice
            }

            let trip = CPTrip(origin: source, destination: destination, routeChoices: choices)
            trip.userInfo = primary

            let estimates = CPTravelEstimates(
                distanceRemaining: Measurement(value: primary.distance, unit: UnitLength.meters),
                timeRemaining: primary.expectedTravelTime
            )
            self.mapTemplate?.updateEstimates(estimates, for: trip)
            self.mapTemplate?.showTripPreviews([trip], textConfiguration: nil)
        }
    }

    func mapTemplate(
        _ mapTemplate: CPMapTemplate,
        selectedPreviewFor trip: CPTrip,
        using routeChoice: CPRouteChoice
    ) {
        if let route = routeChoice.userInfo as? MKRoute {
            activeRoute = route
            mapViewController?.display(route: route)
        }
    }

    func mapTemplate(
        _ mapTemplate: CPMapTemplate,
        startedTrip trip: CPTrip,
        using routeChoice: CPRouteChoice
    ) {
        let route = (routeChoice.userInfo as? MKRoute) ?? activeRoute
        guard let route else { return }

        activeRoute = route
        mapViewController?.display(route: route)
        mapTemplate.hideTripPreviews()

        let session = mapTemplate.startNavigationSession(for: trip)
        navigationSession = session

        let maneuvers = route.steps
            .filter { !$0.instructions.isEmpty }
            .prefix(8)
            .map { step -> CPManeuver in
                let maneuver = CPManeuver()
                maneuver.instructionVariants = [step.instructions]
                maneuver.symbolImage = UIImage(systemName: "arrow.up")
                maneuver.initialTravelEstimates = CPTravelEstimates(
                    distanceRemaining: Measurement(value: step.distance, unit: UnitLength.meters),
                    timeRemaining: max(10, step.distance / 13.4)
                )
                return maneuver
            }

        if maneuvers.isEmpty {
            let fallback = CPManeuver()
            fallback.instructionVariants = ["Continue to destination"]
            fallback.initialTravelEstimates = CPTravelEstimates(
                distanceRemaining: Measurement(value: route.distance, unit: UnitLength.meters),
                timeRemaining: route.expectedTravelTime
            )
            session.upcomingManeuvers = [fallback]
        } else {
            session.upcomingManeuvers = Array(maneuvers)
        }
    }

    func mapTemplateDidCancelNavigation(_ mapTemplate: CPMapTemplate) {
        navigationSession?.cancelTrip()
        navigationSession = nil
        activeRoute = nil
        mapViewController?.mapView.removeOverlays(mapViewController?.mapView.overlays ?? [])
    }

    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let location = locations.last, location.horizontalAccuracy >= 0 else { return }
        currentLocation = location

        if activeRoute == nil {
            mapViewController?.recenter(
                on: location.coordinate,
                heading: location.course >= 0 ? location.course : 0
            )
        }
    }

    private func durationText(_ seconds: TimeInterval) -> String {
        let minutes = max(1, Int(round(seconds / 60)))
        if minutes < 60 { return "\(minutes) min" }
        return "\(minutes / 60) hr \(minutes % 60) min"
    }

    private func distanceText(_ meters: CLLocationDistance) -> String {
        let miles = meters / 1609.344
        return miles < 10 ? String(format: "%.1f mi", miles) : String(format: "%.0f mi", miles)
    }
}
