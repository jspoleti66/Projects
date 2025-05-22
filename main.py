@app.route("/start-stream", methods=["POST"])
def start_stream():
    url = f"{DID_BASE_URL}/talks/streams"
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "source_url": "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png",
        # ⚠️ Elimina "driver_url" o ponelo como cadena vacía
        "config": {
            "fluent": True,
            "pad_audio": 0.2,
        }
    }

    response = requests.post(url, headers=headers, json=body)
    print("RESPONSE:", response.status_code, response.text)  # Debug
    if response.status_code == 201:
        data = response.json()
        stream_id = data.get("id")
        return jsonify({"stream_url": f"wss://api.d-id.com/streams/{stream_id}"})
    else:
        return jsonify({"error": response.text}), 500
