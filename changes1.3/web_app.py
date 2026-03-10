from flask import Flask, render_template, request, jsonify
from huggingface_hub import HfApi
from scan_hf_models import scan_specific_model, scan_models_by_criteria
import os
import html

app = Flask(__name__)

# Initialize Hugging Face API
api = HfApi()

@app.route('/')
def index():
    """Render the main page with the scanning form"""
    return render_template('index.html')

@app.route('/scan_hf_model', methods=['POST'])
def scan_hf_model_web():
    """Scan a specific Hugging Face model"""
    model_url = request.form.get('model_url')
    security_group_uuid = request.form.get('security_group_uuid')
    env_label = request.form.get('env_label', 'default')

    if not security_group_uuid:
        return jsonify({"error": "Security Group UUID is required"}), 400

    if not model_url:
        return jsonify({"error": "Model URL is required"}), 400

    try:
        # Use the existing function but parse the result for web display
        result_text = scan_specific_model(model_url, security_group_uuid, env_label)
        # Parse the result to extract model ID and scan outcome
        if "scan completed:" in result_text:
            parts = result_text.split(" scan completed: ")
            model_id = html.escape(parts[0])
            scan_result = html.escape(parts[1])
            return jsonify({
                "model_id": model_id,
                "scan_result": scan_result,
                "status": "success"
            })
        elif "scan failed:" in result_text:
            parts = result_text.split(" scan failed: ")
            model_id = html.escape(parts[0])
            error = html.escape(parts[1])
            return jsonify({
                "model_id": model_id,
                "error": error,
                "status": "error"
            })
        else:
            return jsonify({
                "result": html.escape(result_text),
                "status": "unknown"
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/scan_local_model', methods=['POST'])
def scan_local_model_web():
    """Scan a local model file"""
    security_group_uuid = request.form.get('security_group_uuid')
    env_label = request.form.get('env_label', 'default')
    model_name = request.form.get('model_name', '')
    model_version = request.form.get('model_version', '')
    model_file = request.files.get('local_model_file')

    if not security_group_uuid:
        return jsonify({"error": "Security Group UUID is required"}), 400

    if not model_file:
        return jsonify({"error": "Model file is required"}), 400

    try:
        # Save the uploaded file temporarily
        import tempfile
        import os
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, model_file.filename)
        model_file.save(temp_file_path)

        # Scan the local model
        from scan_hf_models import scan_local_model
        result_text = scan_local_model(temp_file_path, security_group_uuid, env_label, model_name, model_version)

        # Clean up temporary file
        os.remove(temp_file_path)
        os.rmdir(temp_dir)

        # Parse the result
        if "scan completed:" in result_text:
            parts = result_text.split(" scan completed: ")
            scan_result = html.escape(parts[1] if len(parts) > 1 else result_text)
            return jsonify({
                "scan_result": scan_result,
                "status": "success"
            })
        elif "scan failed:" in result_text:
            parts = result_text.split(" scan failed: ")
            error = html.escape(parts[1] if len(parts) > 1 else result_text)
            return jsonify({
                "error": error,
                "status": "error"
            })
        else:
            return jsonify({
                "result": html.escape(result_text),
                "status": "unknown"
            })
    except Exception as e:
        # Clean up temporary files even if there's an error
        try:
            if 'temp_dir' in locals():
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass
        return jsonify({"error": str(e)}), 500

@app.route('/scan_storage_model', methods=['POST'])
def scan_storage_model_web():
    """Scan a model from object storage"""
    security_group_uuid = request.form.get('security_group_uuid')
    env_label = request.form.get('env_label', 'default')
    storage_uri = request.form.get('storage_uri')
    model_name = request.form.get('model_name', '')
    model_version = request.form.get('model_version', '')
    temp_path = request.form.get('temp_path', '/tmp')

    if not security_group_uuid:
        return jsonify({"error": "Security Group UUID is required"}), 400

    if not storage_uri:
        return jsonify({"error": "Storage URI is required"}), 400

    try:
        # Scan the storage model
        from scan_hf_models import scan_storage_model
        result_text = scan_storage_model(storage_uri, security_group_uuid, env_label, model_name, model_version, temp_path)

        # Parse the result
        if "scan completed:" in result_text:
            parts = result_text.split(" scan completed: ")
            scan_result = html.escape(parts[1] if len(parts) > 1 else result_text)
            return jsonify({
                "scan_result": scan_result,
                "status": "success"
            })
        elif "scan failed:" in result_text:
            parts = result_text.split(" scan failed: ")
            error = html.escape(parts[1] if len(parts) > 1 else result_text)
            return jsonify({
                "error": error,
                "status": "error"
            })
        else:
            return jsonify({
                "result": html.escape(result_text),
                "status": "unknown"
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/scan_by_criteria', methods=['POST'])
def scan_models_by_criteria_web():
    """Scan models based on various criteria from the Hugging Face API"""
    # Get all possible form parameters
    tag = request.form.get('tag', '').strip()
    author = request.form.get('author', '').strip()
    model_name = request.form.get('model_name', '').strip()
    search = request.form.get('search', '').strip()
    trained_dataset = request.form.get('trained_dataset', '').strip()
    library = request.form.get('library', '').strip()
    language = request.form.get('language', '').strip()
    tags = request.form.get('tags', '').strip()
    limit_str = request.form.get('limit', '').strip()
    sort = request.form.get('sort', '').strip()
    direction_str = request.form.get('direction', '').strip()
    security_group_uuid = request.form.get('security_group_uuid', '').strip()
    env_label = request.form.get('env_label', 'default')

    if not security_group_uuid:
        return jsonify({"error": "Security Group UUID is required"}), 400

    # Convert limit to integer if provided
    limit = None
    if limit_str and limit_str.isdigit():
        limit = int(limit_str)

    # Convert direction to integer if provided
    direction = None
    if direction_str == "desc":
        direction = -1
    elif direction_str == "asc":
        direction = 1

    try:
        # Use the enhanced function with all parameters
        results_text = scan_models_by_criteria(
            tag=tag if tag else None,
            author=author if author else None,
            model_name=model_name if model_name else None,
            search=search if search else None,
            trained_dataset=trained_dataset if trained_dataset else None,
            library=library if library else None,
            language=language if language else None,
            tags=tags if tags else None,
            limit=limit,
            sort=sort if sort else None,
            direction=direction,
            security_group_uuid=security_group_uuid,
            env_label=env_label
        )

        # Parse results for web display
        parsed_results = []
        for result_text in results_text:
            if "scan completed:" in result_text:
                parts = result_text.split(" scan completed: ")
                model_id = html.escape(parts[0])
                scan_result = html.escape(parts[1])
                parsed_results.append({
                    "model_id": model_id,
                    "scan_result": scan_result,
                    "status": "success"
                })
            elif "scan failed:" in result_text:
                parts = result_text.split(" scan failed: ")
                model_id = html.escape(parts[0])
                error = html.escape(parts[1])
                parsed_results.append({
                    "model_id": model_id,
                    "error": error,
                    "status": "error"
                })
            else:
                parsed_results.append({
                    "result": html.escape(result_text),
                    "status": "unknown"
                })

        return jsonify({
            "models_scanned": len(parsed_results),
            "results": parsed_results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)