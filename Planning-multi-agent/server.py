from flask import Flask, render_template, request, jsonify
from RAG_Pipeline_Smartphone import execute_rag_pipeline
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

    @app.route('/analyze', methods=['POST'])
    def analyze():
        device = request.json.get('device')
            if not device:
                    return jsonify({"error": "No device name provided"}), 400

                            try:
                                    report = execute_rag_pipeline(device, output_format='html')
                                            return jsonify({"report": report})
                                                except Exception as e:
                                                        return jsonify({"error": str(e)}), 500

                                                        if __name__ == '__main__':
                                                            if not os.path.exists('templates'):
                                                                    os.makedirs('templates')
                                                                        app.run(debug=True, port=5000)
                                                                        
