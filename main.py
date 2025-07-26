from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/', methods=['POST'])
def get_direct_url():
    try:
        data = request.get_json()
        video_url = data.get('url')
        if not video_url:
            return jsonify({'error': 'Missing URL'}), 400

        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'forceurl': True,
            'format': 'bestvideo+bestaudio/best[ext=m3u8]'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({'direct_url': info['url']})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000)