from django.http import HttpResponse
import time

class BlockedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Login করা user চেক করো
        if request.user.is_authenticated:
            if not request.user.is_active:
                # Infinite loading এর জন্য — response পাঠাবে না
                # বরং একটা never-ending streaming response দেবে
                return self._infinite_response(request)
        
        response = self.get_response(request)
        return response

    def _infinite_response(self, request):
        # HTML page যেটা JavaScript দিয়ে infinite loading দেখাবে
        html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Loading...</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #000a02;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            font-family: monospace;
            color: #00ff41;
        }
        .loader {
            text-align: center;
        }
        .spinner {
            width: 50px;
            height: 50px;
            border: 3px solid #003b10;
            border-top: 3px solid #00ff41;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
            box-shadow: 0 0 15px rgba(0,255,65,0.3);
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .text {
            font-size: 12px;
            letter-spacing: 3px;
            color: #005a18;
            animation: blink 2s ease infinite;
        }
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
    </style>
</head>
<body>
    <div class="loader">
        <div class="spinner"></div>
        <div class="text">CONNECTING TO SERVER...</div>
    </div>
    <script>
        // কখনো শেষ হবে না
        function neverEnd() {
            return new Promise(() => {});
        }
        neverEnd();
        
        // Page unload ও prevent করো
        window.onbeforeunload = function() {
            return "Loading...";
        };
    </script>
</body>
</html>
        """
        return HttpResponse(html, status=200)
