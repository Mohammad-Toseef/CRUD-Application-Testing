import os.path
import pdfkit

html_content = u"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
    body {
            font-family: "Segoe UI";
                                            }
</style>
</head>
<body>
🎉 ➡️ 👋 🐞
</body>
</style>
</html>
"""

pdfkit.from_string(html_content, 'out.pdf')

