#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GNTM Web界面
提供简单的Web图形界面用于生成文本图像
"""

import os
import sys
import json
import subprocess
import threading
import time
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import webbrowser

class GTNMWebHandler(BaseHTTPRequestHandler):
    """GNTM Web请求处理器"""
    
    def do_GET(self):
        """处理GET请求"""
        path = urlparse(self.path).path
        
        if path == '/' or path == '/index.html':
            self.serve_index()
        elif path == '/api/status':
            self.serve_status()
        elif path == '/api/fonts':
            self.serve_fonts()
        elif path == '/api/corpus':
            self.serve_corpus()
        elif path.startswith('/output/'):
            self.serve_output(path)
        else:
            self.send_error(404)
    
    def do_POST(self):
        """处理POST请求"""
        path = urlparse(self.path).path
        
        if path == '/api/generate':
            self.handle_generate()
        else:
            self.send_error(404)
    
    def serve_index(self):
        """服务主页"""
        html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GNTM - Web界面</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; opacity: 0.9; }
        
        .content { padding: 40px; }
        .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
        .form-group { margin-bottom: 25px; }
        .form-group label { 
            display: block; 
            margin-bottom: 8px; 
            font-weight: 600;
            color: #333;
        }
        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e8ed;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .btn:hover { transform: translateY(-2px); }
        .btn:disabled { 
            opacity: 0.6; 
            cursor: not-allowed;
            transform: none;
        }
        
        .results {
            margin-top: 40px;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 12px;
            display: none;
        }
        .results.show { display: block; }
        
        .status {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-weight: 500;
        }
        .status.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .status.info { background: #cce7f0; color: #0c5460; border: 1px solid #b8daff; }
        
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .gallery img {
            width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .gallery img:hover { transform: scale(1.05); }
        
        @media (max-width: 768px) {
            .form-grid { grid-template-columns: 1fr; gap: 20px; }
            .container { margin: 10px; }
            .content { padding: 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 GNTM</h1>
            <p>Generative but Natural TextImage Maker - Web界面</p>
        </div>
        
        <div class="content">
            <form id="generateForm">
                <div class="form-grid">
                    <div>
                        <div class="form-group">
                            <label for="language">语言</label>
                            <select id="language" name="language">
                                <option value="ch">中文</option>
                                <option value="en">英文</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="fonts">字体目录</label>
                            <select id="fonts" name="fonts">
                                <option value="ch">中文字体 (fonts/ch/)</option>
                                <option value="en">英文字体 (fonts/en/)</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="count">图片数量</label>
                            <input type="number" id="count" name="count" value="50" min="1" max="1000">
                        </div>
                        
                        <div class="form-group">
                            <label for="size">字体大小</label>
                            <input type="number" id="size" name="size" value="32" min="16" max="128">
                        </div>
                    </div>
                    
                    <div>
                        <div class="form-group">
                            <label for="corpus">文本内容 (每行一个)</label>
                            <textarea id="corpus" name="corpus" rows="6" placeholder="你好世界&#10;机器学习&#10;深度学习"></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="extension">图片格式</label>
                            <select id="extension" name="extension">
                                <option value="jpg">JPG (小文件)</option>
                                <option value="png">PNG (高质量)</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="skew_angle">倾斜角度</label>
                            <input type="number" id="skew_angle" name="skew_angle" value="10" min="0" max="30">
                        </div>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <button type="submit" class="btn" id="generateBtn">
                        🚀 开始生成
                    </button>
                </div>
            </form>
            
            <div id="results" class="results">
                <div id="status"></div>
                <div id="gallery" class="gallery"></div>
            </div>
        </div>
    </div>

    <script>
        const form = document.getElementById('generateForm');
        const results = document.getElementById('results');
        const status = document.getElementById('status');
        const gallery = document.getElementById('gallery');
        const generateBtn = document.getElementById('generateBtn');
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            generateBtn.disabled = true;
            generateBtn.textContent = '⏳ 生成中...';
            results.classList.add('show');
            status.className = 'status info';
            status.textContent = '正在生成图片，请稍候...';
            gallery.innerHTML = '';
            
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    status.className = 'status success';
                    status.textContent = `✅ 生成完成！共生成 ${result.count} 张图片`;
                    
                    // 显示图片预览
                    if (result.images && result.images.length > 0) {
                        gallery.innerHTML = '';
                        result.images.slice(0, 20).forEach(img => {
                            const imgEl = document.createElement('img');
                            imgEl.src = img;
                            imgEl.alt = '生成的图片';
                            gallery.appendChild(imgEl);
                        });
                    }
                } else {
                    status.className = 'status error';
                    status.textContent = `❌ 生成失败: ${result.error}`;
                }
            } catch (error) {
                status.className = 'status error';
                status.textContent = `❌ 请求失败: ${error.message}`;
            }
            
            generateBtn.disabled = false;
            generateBtn.textContent = '🚀 开始生成';
        });
        
        // 语言切换时自动更新字体
        document.getElementById('language').addEventListener('change', (e) => {
            document.getElementById('fonts').value = e.target.value;
        });
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_status(self):
        """服务状态API"""
        from core.diagnostics import GTNMDiagnostics
        
        checks = GTNMDiagnostics.check_environment()
        status = {
            'environment': [
                {'name': name, 'ok': ok, 'message': msg}
                for name, ok, msg in checks
            ],
            'fonts': {},
            'ready': all(ok for _, ok, _ in checks)
        }
        
        # 检查字体
        for font_dir in ['ch', 'en']:
            ok, fonts, msg = GTNMDiagnostics.check_fonts(font_dir)
            status['fonts'][font_dir] = {
                'ok': ok,
                'count': len(fonts),
                'message': msg
            }
        
        self.send_json(status)
    
    def serve_fonts(self):
        """服务字体列表API"""
        fonts = {}
        for font_dir in ['ch', 'en']:
            ok, font_list, msg = GTNMDiagnostics.check_fonts(font_dir)
            fonts[font_dir] = font_list if ok else []
        
        self.send_json(fonts)
    
    def serve_corpus(self):
        """服务语料库列表API"""
        corpus_files = []
        texts_dir = Path('texts')
        if texts_dir.exists():
            for file in texts_dir.glob('*.txt'):
                corpus_files.append(str(file))
        
        self.send_json(corpus_files)
    
    def serve_output(self, path):
        """服务输出文件"""
        file_path = Path(path[1:])  # 移除开头的 /
        
        if not file_path.exists():
            self.send_error(404)
            return
        
        # 确定MIME类型
        if file_path.suffix.lower() in ['.jpg', '.jpeg']:
            content_type = 'image/jpeg'
        elif file_path.suffix.lower() == '.png':
            content_type = 'image/png'
        else:
            content_type = 'application/octet-stream'
        
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()
        
        with open(file_path, 'rb') as f:
            self.wfile.write(f.read())
    
    def handle_generate(self):
        """处理生成请求"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            # 创建临时语料库文件
            corpus_content = data.get('corpus', '').strip()
            if not corpus_content:
                self.send_json({'success': False, 'error': '请输入文本内容'})
                return
            
            temp_corpus = Path('temp_web_corpus.txt')
            with open(temp_corpus, 'w', encoding='utf-8') as f:
                f.write(corpus_content)
            
            # 构建命令
            cmd = [
                sys.executable, 'run.py',
                '--language', data.get('language', 'ch'),
                '--fonts', data.get('fonts', 'ch'),
                '--corpus', str(temp_corpus),
                '--count', str(data.get('count', 50)),
                '--size', str(data.get('size', 32)),
                '--extension', data.get('extension', 'jpg'),
                '--skew_angle', str(data.get('skew_angle', 10)),
                '--output_dir', 'output/web_generated',
                '--num_workers', '4'
            ]
            
            # 执行生成
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=300  # 5分钟超时
            )
            
            # 清理临时文件
            if temp_corpus.exists():
                temp_corpus.unlink()
            
            if result.returncode == 0:
                # 获取生成的图片列表
                output_dir = Path('output/web_generated')
                images = []
                if output_dir.exists():
                    for img in output_dir.glob(f"*.{data.get('extension', 'jpg')}"):
                        images.append(f"/{img}")
                
                self.send_json({
                    'success': True,
                    'count': len(images),
                    'images': images[:20],  # 只返回前20张用于预览
                    'output_dir': str(output_dir)
                })
            else:
                self.send_json({
                    'success': False,
                    'error': result.stderr or result.stdout or '生成失败'
                })
                
        except json.JSONDecodeError:
            self.send_json({'success': False, 'error': '无效的JSON数据'})
        except subprocess.TimeoutExpired:
            self.send_json({'success': False, 'error': '生成超时，请减少图片数量'})
        except Exception as e:
            self.send_json({'success': False, 'error': str(e)})
    
    def send_json(self, data):
        """发送JSON响应"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def log_message(self, format, *args):
        """禁用访问日志"""
        pass

def run_server(port=8080):
    """运行Web服务器"""
    try:
        server = HTTPServer(('localhost', port), GTNMWebHandler)
        print(f"🌐 GNTM Web界面已启动")
        print(f"📍 访问地址: http://localhost:{port}")
        print(f"🔧 按 Ctrl+C 停止服务器")
        
        # 自动打开浏览器
        threading.Timer(1, lambda: webbrowser.open(f'http://localhost:{port}')).start()
        
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Web服务器已停止")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ 端口 {port} 已被占用，尝试使用其他端口:")
            print(f"   python web_interface.py --port {port + 1}")
        else:
            print(f"❌ 启动服务器失败: {e}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="GNTM Web界面")
    parser.add_argument('--port', type=int, default=8080, help='端口号 (默认: 8080)')
    args = parser.parse_args()
    
    # 检查是否在正确的目录
    if not Path('run.py').exists():
        print("❌ 请在项目根目录运行此脚本")
        print("   cd /path/to/data-gen")
        print("   python web_interface.py")
        sys.exit(1)
    
    run_server(args.port)

if __name__ == '__main__':
    main()
