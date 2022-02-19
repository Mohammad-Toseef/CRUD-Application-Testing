import os.path
import pdfkit

html_content = u"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
    body {
            font-family: "Segoe UI Emoji",
                        Times, Symbola, Aegyptus, Code2000, Code2001, Code2002, Musica, serif,
                                    LastResort, 'Ubuntu', sans-serif;
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

