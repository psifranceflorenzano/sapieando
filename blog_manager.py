#!/usr/bin/env python3
"""
Blog Post Manager Web Application
Manages Jekyll blog posts through a simple web interface.
Works on any OS with a web browser.
"""

import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = 'blog-manager-secret-key-change-in-production'

# Get the workspace directory
WORKSPACE_DIR = Path(__file__).parent.absolute()
POSTS_DIR = WORKSPACE_DIR / "_posts"
CONFIG_FILE = WORKSPACE_DIR / "_config.yml"


class PostManager:
    """Manages blog post files - parsing, writing, and listing."""
    
    def __init__(self, posts_dir: Path = POSTS_DIR):
        self.posts_dir = posts_dir
        self.posts_dir.mkdir(exist_ok=True)
    
    def parse_post_file(self, filepath: Path) -> Dict:
        """Parse a markdown post file and extract front matter and content."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract front matter
        if not content.startswith('---'):
            return None
        
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None
        
        front_matter_str = parts[1].strip()
        body = parts[2].strip()
        
        try:
            front_matter = yaml.safe_load(front_matter_str)
        except:
            return None
        
        return {
            'title': front_matter.get('title', ''),
            'date': front_matter.get('date', ''),
            'author': front_matter.get('author', ''),
            'categories': front_matter.get('categories', []),
            'excerpt': front_matter.get('excerpt', ''),
            'content': body,
            'filename': filepath.name
        }
    
    def generate_filename(self, title: str, date: str) -> str:
        """Generate filename from title and date."""
        # Convert date to YYYY-MM-DD format
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            date_str = date_obj.strftime('%Y-%m-%d')
        except:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        # Slugify title
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        slug = slug.strip('-')
        
        return f"{date_str}-{slug}.md"
    
    def write_post_file(self, filename: str, title: str, author: str, 
                       categories: List[str], excerpt: str, date: str, content: str):
        """Write a post file with front matter matching Jekyll format."""
        filepath = self.posts_dir / filename
        
        # Ensure date is in YYYY-MM-DD format (Jekyll expects this format, unquoted)
        try:
            # Parse and reformat date to ensure consistency
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            date_str = date_obj.strftime('%Y-%m-%d')
        except:
            date_str = date  # Use as-is if parsing fails
        
        # Format front matter to match Jekyll expectations exactly
        # Match the format of the working post: title and excerpt quoted, date unquoted, categories as array
        # Categories should be formatted as ["Cat1", "Cat2"] - YAML array format
        categories_str = '[' + ', '.join([f'"{cat}"' for cat in categories]) + ']'
        
        front_matter_lines = [
            '---',
            f'title: "{title}"',
            f'date: {date_str}',  # Unquoted date (Jekyll prefers this)
            f'author: "{author}"',
            f'categories: {categories_str}',  # Array format like ["Cat1", "Cat2"]
            f'excerpt: "{excerpt}"',
            '---'
        ]
        
        file_content = '\n'.join(front_matter_lines) + '\n\n' + content + '\n'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(file_content)
    
    def list_posts(self) -> List[Dict]:
        """List all posts."""
        posts = []
        for filepath in sorted(self.posts_dir.glob('*.md'), reverse=True):
            post = self.parse_post_file(filepath)
            if post:
                posts.append(post)
        return posts
    
    def delete_post(self, filename: str) -> bool:
        """Delete a post file."""
        filepath = self.posts_dir / filename
        if filepath.exists():
            filepath.unlink()
            return True
        return False


class GitManager:
    """Manages git operations."""
    
    def __init__(self, workspace_dir: Path = WORKSPACE_DIR):
        self.workspace_dir = workspace_dir
    
    def commit_changes(self, message: str) -> bool:
        """Commit changes to git."""
        try:
            subprocess.run(
                ['git', 'add', '_posts/'],
                cwd=self.workspace_dir,
                check=True,
                capture_output=True
            )
            subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=self.workspace_dir,
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    def push_changes(self) -> bool:
        """Push changes to remote."""
        try:
            subprocess.run(
                ['git', 'push'],
                cwd=self.workspace_dir,
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False


class JekyllManager:
    """Manages Jekyll build operations."""
    
    def __init__(self, workspace_dir: Path = WORKSPACE_DIR):
        self.workspace_dir = workspace_dir
    
    def build_site(self) -> Tuple[bool, str]:
        """
        Trigger Jekyll build to regenerate pages.
        Returns (success, message)
        """
        try:
            # Check if bundle/jekyll is available
            result = subprocess.run(
                ['which', 'bundle'],
                cwd=self.workspace_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return False, "Jekyll não encontrado. Execute 'bundle install' primeiro."
            
            # Try to build with bundle exec jekyll build
            # Clean build to avoid conflicts with excluded folders
            build_result = subprocess.run(
                ['bundle', 'exec', 'jekyll', 'build'],
                cwd=self.workspace_dir,
                capture_output=True,
                text=True,
                timeout=60  # 60 second timeout
            )
            
            if build_result.returncode == 0:
                return True, "Site Jekyll reconstruído com sucesso!"
            else:
                error_msg = build_result.stderr[:200] if build_result.stderr else "Erro desconhecido"
                return False, f"Erro ao construir site: {error_msg}"
                
        except subprocess.TimeoutExpired:
            return False, "Timeout ao construir site Jekyll"
        except FileNotFoundError:
            return False, "Jekyll não está instalado. Instale com: gem install bundler && bundle install"
        except Exception as e:
            return False, f"Erro ao construir site: {str(e)}"
    
    def is_jekyll_available(self) -> bool:
        """Check if Jekyll is available."""
        try:
            result = subprocess.run(
                ['which', 'bundle'],
                cwd=self.workspace_dir,
                capture_output=True
            )
            return result.returncode == 0
        except:
            return False


def load_default_author() -> str:
    """Load default author from _config.yml."""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config.get('author', {}).get('name', 'France Florenzano')
    except:
        pass
    return 'France Florenzano'


@app.route('/')
def index():
    """Main page - list all posts."""
    post_manager = PostManager()
    posts = post_manager.list_posts()
    return render_template('index.html', posts=posts)


@app.route('/new', methods=['GET', 'POST'])
def new_post():
    """Create a new post."""
    post_manager = PostManager()
    git_manager = GitManager()
    jekyll_manager = JekyllManager()
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        categories_str = request.form.get('categories', '').strip()
        categories = [cat.strip() for cat in categories_str.split(',') if cat.strip()]
        excerpt = request.form.get('excerpt', '').strip()
        date = request.form.get('date', '').strip()
        content = request.form.get('content', '').strip()
        
        # Validation
        if not all([title, author, categories, excerpt, date, content]):
            flash('Todos os campos são obrigatórios', 'error')
            return render_template('edit.html', 
                                 post_data=None,
                                 default_author=load_default_author(),
                                 today=datetime.now().strftime('%Y-%m-%d'))
        
        # Generate filename
        filename = post_manager.generate_filename(title, date)
        
        # Write file
        post_manager.write_post_file(filename, title, author, categories, excerpt, date, content)
        
        # Build Jekyll site locally
        jekyll_success, jekyll_msg = jekyll_manager.build_site()
        if jekyll_success:
            flash(f'Post criado! {jekyll_msg}', 'success')
        else:
            flash(f'Post criado, mas Jekyll build falhou: {jekyll_msg}', 'warning')
        
        # Git operations
        commit_message = f"Adicionar post: {title}"
        if git_manager.commit_changes(commit_message):
            git_manager.push_changes()
            flash('Alterações enviadas para o repositório GitHub!', 'success')
        else:
            flash('Post criado localmente, mas houve um erro ao fazer commit/push no git.', 'warning')
        
        return redirect(url_for('index'))
    
    # GET request - show form
    return render_template('edit.html',
                         post_data=None,
                         default_author=load_default_author(),
                         today=datetime.now().strftime('%Y-%m-%d'))


@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit_post(filename):
    """Edit an existing post."""
    post_manager = PostManager()
    git_manager = GitManager()
    jekyll_manager = JekyllManager()
    
    filepath = POSTS_DIR / filename
    if not filepath.exists():
        flash('Post não encontrado', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        categories_str = request.form.get('categories', '').strip()
        categories = [cat.strip() for cat in categories_str.split(',') if cat.strip()]
        excerpt = request.form.get('excerpt', '').strip()
        date = request.form.get('date', '').strip()
        content = request.form.get('content', '').strip()
        
        # Validation
        if not all([title, author, categories, excerpt, date, content]):
            flash('Todos os campos são obrigatórios', 'error')
            post_data = post_manager.parse_post_file(filepath)
            return render_template('edit.html',
                                 post_data=post_data,
                                 default_author=load_default_author(),
                                 today=datetime.now().strftime('%Y-%m-%d'))
        
        # Generate new filename if date changed
        new_filename = post_manager.generate_filename(title, date)
        
        # Delete old file if filename changed
        if new_filename != filename:
            post_manager.delete_post(filename)
        
        # Write file
        post_manager.write_post_file(new_filename, title, author, categories, excerpt, date, content)
        
        # Build Jekyll site locally
        jekyll_success, jekyll_msg = jekyll_manager.build_site()
        if jekyll_success:
            flash(f'Post editado! {jekyll_msg}', 'success')
        else:
            flash(f'Post editado, mas Jekyll build falhou: {jekyll_msg}', 'warning')
        
        # Git operations
        commit_message = f"Editar post: {title}"
        if git_manager.commit_changes(commit_message):
            git_manager.push_changes()
            flash('Alterações enviadas para o repositório GitHub!', 'success')
        else:
            flash('Post editado localmente, mas houve um erro ao fazer commit/push no git.', 'warning')
        
        return redirect(url_for('index'))
    
    # GET request - show form with existing data
    post_data = post_manager.parse_post_file(filepath)
    if not post_data:
        flash('Erro ao ler o post', 'error')
        return redirect(url_for('index'))
    
    return render_template('edit.html',
                         post_data=post_data,
                         default_author=load_default_author(),
                         today=datetime.now().strftime('%Y-%m-%d'))


@app.route('/delete/<filename>', methods=['POST'])
def delete_post(filename):
    """Delete a post."""
    post_manager = PostManager()
    git_manager = GitManager()
    jekyll_manager = JekyllManager()
    
    filepath = POSTS_DIR / filename
    if not filepath.exists():
        flash('Post não encontrado', 'error')
        return redirect(url_for('index'))
    
    # Get post title for commit message
    post_data = post_manager.parse_post_file(filepath)
    title = post_data.get('title', filename) if post_data else filename
    
    # Delete file
    if post_manager.delete_post(filename):
        # Build Jekyll site locally (to remove the page)
        jekyll_success, jekyll_msg = jekyll_manager.build_site()
        if jekyll_success:
            flash(f'Post removido! {jekyll_msg}', 'success')
        else:
            flash(f'Post removido, mas Jekyll build falhou: {jekyll_msg}', 'warning')
        
        # Git operations
        commit_message = f"Remover post: {title}"
        if git_manager.commit_changes(commit_message):
            git_manager.push_changes()
            flash('Alterações enviadas para o repositório GitHub!', 'success')
        else:
            flash('Post removido localmente, mas houve um erro ao fazer commit/push no git.', 'warning')
    else:
        flash('Erro ao remover o post', 'error')
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    jekyll_manager = JekyllManager()
    jekyll_available = jekyll_manager.is_jekyll_available()
    
    print("\n" + "="*60)
    print("Blog Post Manager - Web Interface")
    print("="*60)
    print(f"\nAcesse: http://127.0.0.1:5000")
    
    if jekyll_available:
        print("\n✓ Jekyll detectado - páginas serão geradas automaticamente")
        print("  Para ver o site localmente, execute em outro terminal:")
        print("  bundle exec jekyll serve")
        print("  Depois acesse: http://localhost:4000")
    else:
        print("\n⚠ Jekyll não encontrado")
        print("  Para gerar páginas localmente, instale Jekyll:")
        print("  gem install bundler && bundle install")
    
    print("\nPressione Ctrl+C para parar o servidor\n")
    print("="*60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
