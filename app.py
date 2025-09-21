import logging
import os
import torch
from flask import Flask, request, jsonify
from FlagEmbedding import BGEM3FlagModel
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
model = None

def load_model():
    global model
    try:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        logger.info(f"Loading BGE-M3 model on {device}...")
        model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True, device=device)
        logger.info(f"Model loaded successfully on {device}")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "model_loaded": model is not None})

@app.route('/embed', methods=['POST'])
def embed_text():
    try:
        data = request.get_json()
        if not data or 'texts' not in data:
            return jsonify({"error": "Missing 'texts' field"}), 400
        
        texts = data['texts']
        if isinstance(texts, str):
            texts = [texts]
        
        logger.info(f"Processing {len(texts)} text(s) for embeddings")
        
        embeddings = model.encode(texts, batch_size=12, max_length=8192)['dense_vecs']
        embeddings_list = [emb.tolist() for emb in embeddings]
        
        return jsonify({
            "embeddings": embeddings_list,
            "dimension": len(embeddings_list[0]) if embeddings_list else 0,
            "count": len(embeddings_list)
        })
        
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/embed/batch', methods=['POST'])
def embed_batch():
    try:
        data = request.get_json()
        if not data or 'texts' not in data:
            return jsonify({"error": "Missing 'texts' field"}), 400
        
        texts = data['texts']
        batch_size = data.get('batch_size', 32)
        
        logger.info(f"Processing batch of {len(texts)} texts")
        
        embeddings = model.encode(texts, batch_size=batch_size, max_length=8192)['dense_vecs']
        embeddings_list = [emb.tolist() for emb in embeddings]
        
        return jsonify({
            "embeddings": embeddings_list,
            "dimension": len(embeddings_list[0]) if embeddings_list else 0,
            "count": len(embeddings_list)
        })
        
    except Exception as e:
        logger.error(f"Error in batch processing: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    load_model()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
