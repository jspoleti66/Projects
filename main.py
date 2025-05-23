@app.route("/create_stream", methods=["POST"])
def create_stream():
    user_text = request.json.get("text", "Hola, soy tu clon AlmostMe")

    headers = {
        "Authorization": f"Bearer {DID_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "source_url": "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png",
        "config": {
            "stitch": True,
            "driver_expressions": {
                "expressions": [
                    {"expression": "happy", "start_frame": 0, "intensity": 0.4}
                ]
            },
        },
        "script": {
            "type": "text",
            "input": user_text,
            "provider": {"type": "microsoft", "voice_id": "es-ES-AlvaroNeural"},
            "ssml": False
        }
    }

    response = requests.post("https://api.d-id.com/talks/streams", headers=headers, json=body)
    data = response.json()

    # Log para debug:
    print("D-ID API Response:", data)

    stream_id = data.get("id")
    sdp_offer = data.get("offer")
    ice_servers = data.get("ice_servers", [])

    if not sdp_offer:
        # Si no vino offer, devolver error
        return jsonify({"error": "No SDP offer from D-ID API", "details": data}), 500

    return jsonify({
        "streamId": stream_id,
        "sdp": sdp_offer,
        "iceServers": ice_servers
    })
