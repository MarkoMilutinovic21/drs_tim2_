"""
Generic proxy routes for flight-service resources.
"""
import os
import requests
from threading import Thread
from flask import Blueprint, Response, current_app, jsonify, request
from app import socketio

proxy_bp = Blueprint('proxy', __name__)
_PROXIED_PREFIXES = ('flights', 'bookings', 'ratings')


def _build_candidate_urls(configured_service_url: str):
    in_docker = os.path.exists('/.dockerenv')
    if 'localhost' in configured_service_url or '127.0.0.1' in configured_service_url:
        candidate_base_urls = (
            ['http://flight-service:5001']
            if in_docker
            else [configured_service_url, 'http://flight-service:5001']
        )
    elif 'flight-service' in configured_service_url:
        candidate_base_urls = [configured_service_url, 'http://localhost:5001']
    else:
        candidate_base_urls = [configured_service_url]

    seen = set()
    return [url for url in candidate_base_urls if not (url in seen or seen.add(url))]


def _send_report_async(app, candidate_base_urls, params, body, headers):
    with app.app_context():
        for base_url in candidate_base_urls:
            target_url = f"{base_url}/api/flights/report"
            try:
                response = requests.post(
                    url=target_url,
                    params=params,
                    data=body,
                    headers=headers,
                    timeout=(2, 60)
                )
                if response.status_code < 400:
                    return
                app.logger.error(
                    f"Async report proxy failed for {target_url}: {response.status_code} {response.text}"
                )
            except requests.RequestException as exc:
                app.logger.error(f"Async report proxy failed for {target_url}: {exc}")


@proxy_bp.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'])
def proxy_to_flight_service(path):
    if request.headers.get('X-Flight-Proxy-Hop') == '1':
        return jsonify({'error': 'Proxy loop detected'}), 502

    first_segment = path.split('/', 1)[0]
    if first_segment not in _PROXIED_PREFIXES:
        return jsonify({'error': 'Not found'}), 404

    configured_service_url = current_app.config['FLIGHT_SERVICE_URL'].rstrip('/')
    candidate_base_urls = _build_candidate_urls(configured_service_url)

    headers = {}
    for header_name in ('Authorization', 'Content-Type', 'Accept'):
        header_value = request.headers.get(header_name)
        if header_value:
            headers[header_name] = header_value
    headers['X-Flight-Proxy-Hop'] = '1'

    last_error = None
    downstream = None
    target_path = f"/api/{path}"
    forwarded_params = request.args.to_dict(flat=False)
    if request.method == 'GET' and path == 'ratings':
        # Avoid server->flight-service->server recursive lookups through proxy.
        forwarded_params['include_user_details'] = ['false']

    if request.method == 'POST' and path == 'flights/report':
        app = current_app._get_current_object()
        thread = Thread(
            target=_send_report_async,
            args=(app, candidate_base_urls, forwarded_params, request.get_data(), headers),
            daemon=True
        )
        thread.start()
        return jsonify({'message': 'Report generation started'}), 202
    for base_url in candidate_base_urls:
        target_url = f"{base_url}{target_path}"
        try:
            downstream = requests.request(
                method=request.method,
                url=target_url,
                params=forwarded_params,
                data=request.get_data(),
                headers=headers,
                timeout=(2, 15)
            )
            break
        except requests.RequestException as exc:
            last_error = exc
            current_app.logger.error(f"Proxy forward failed for {target_url}: {exc}")

    if downstream is None:
        return jsonify({
            'error': 'Flight service unavailable',
            'details': str(last_error) if last_error else 'unknown'
        }), 502

    # Keep existing realtime UX when traffic is routed through server.
    if first_segment == 'flights' and downstream.status_code in (200, 201):
        try:
            data = downstream.json() if downstream.content else {}
        except ValueError:
            data = {}

        is_create = request.method == 'POST' and path == 'flights'
        is_update = request.method == 'PUT' and path.count('/') == 1 and path.startswith('flights/')
        is_approve = request.method == 'POST' and path.endswith('/approve')

        if is_create or is_update:
            flight_data = data.get('flight')
            if flight_data:
                socketio.emit('new_flight', flight_data, namespace='/')

        if is_approve:
            flight_data = data.get('flight') or {}
            flight_id = int(path.split('/')[1]) if path.split('/')[1].isdigit() else None
            socketio.emit('flight_status_changed', {
                'flight_id': flight_id,
                'status': flight_data.get('status'),
                'rejection_reason': flight_data.get('rejection_reason')
            }, namespace='/')

    content_type = downstream.headers.get('Content-Type', 'application/json')
    return Response(
        response=downstream.content,
        status=downstream.status_code,
        content_type=content_type
    )
