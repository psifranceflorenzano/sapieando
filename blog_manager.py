#!/usr/bin/env python3
"""
Blog Post Manager GUI Application
Manages Jekyll blog posts through a user-friendly GUI interface.
"""

import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml
import customtkinter as ctk
from tkinter import messagebox

# Set appearance mode and color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

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
        """
        Parse a markdown post file and extract front matter and content.
        
        Returns:
            dict with keys: title, date, author, categories, excerpt, content, filename
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract front matter (between --- markers)
            front_matter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
            
            if not front_matter_match:
                raise ValueError("Invalid post format: missing front matter")
            
            front_matter_text = front_matter_match.group(1)
            post_content = front_matter_match.group(2)
            
            # Parse YAML front matter
            front_matter = yaml.safe_load(front_matter_text)
            
            return {
                'title': front_matter.get('title', ''),
                'date': front_matter.get('date', ''),
                'author': front_matter.get('author', ''),
                'categories': front_matter.get('categories', []),
                'excerpt': front_matter.get('excerpt', ''),
                'content': post_content.strip(),
                'filename': filepath.name
            }
        except Exception as e:
            raise ValueError(f"Error parsing post file: {str(e)}")
    
    def generate_filename(self, title: str, date: str) -> str:
        """
        Generate a filename slug from title and date.
        Format: YYYY-MM-DD-title-slug.md
        """
        # Convert date to YYYY-MM-DD format if needed
        if isinstance(date, str):
            try:
                # Try parsing different date formats
                if len(date) == 10:  # YYYY-MM-DD
                    date_str = date
                else:
                    dt = datetime.strptime(date, '%Y-%m-%d')
                    date_str = dt.strftime('%Y-%m-%d')
            except:
                date_str = datetime.now().strftime('%Y-%m-%d')
        else:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        # Create slug from title
        slug = title.lower()
        # Replace spaces and special chars with hyphens
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        slug = slug.strip('-')
        
        # Limit slug length
        if len(slug) > 50:
            slug = slug[:50]
        
        return f"{date_str}-{slug}.md"
    
    def write_post_file(self, filepath: Path, post_data: Dict) -> None:
        """
        Write a post to a markdown file with proper front matter formatting.
        
        Args:
            filepath: Path to the output file
            post_data: Dict with keys: title, date, author, categories, excerpt, content
        """
        # Prepare front matter
        front_matter = {
            'title': post_data['title'],
            'date': post_data['date'],
            'author': post_data['author'],
            'categories': post_data['categories'],
            'excerpt': post_data['excerpt']
        }
        
        # Format front matter as YAML
        yaml_content = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('---\n')
            f.write(yaml_content)
            f.write('---\n\n')
            f.write(post_data['content'])
            if not post_data['content'].endswith('\n'):
                f.write('\n')
    
    def list_posts(self) -> List[Dict]:
        """
        List all posts in the _posts directory.
        
        Returns:
            List of dicts with post metadata (title, date, filename)
        """
        posts = []
        
        if not self.posts_dir.exists():
            return posts
        
        for filepath in sorted(self.posts_dir.glob('*.md'), reverse=True):
            try:
                post_data = self.parse_post_file(filepath)
                posts.append({
                    'title': post_data['title'],
                    'date': post_data['date'],
                    'filename': post_data['filename'],
                    'filepath': filepath
                })
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
                continue
        
        return posts
    
    def delete_post(self, filepath: Path) -> bool:
        """Delete a post file."""
        try:
            if filepath.exists():
                filepath.unlink()
                return True
            return False
        except Exception as e:
            raise Exception(f"Error deleting post: {str(e)}")


class GitManager:
    """Manages git operations for committing and pushing changes."""
    
    def __init__(self, repo_dir: Path = WORKSPACE_DIR):
        self.repo_dir = repo_dir
    
    def commit_changes(self, message: str) -> Tuple[bool, str]:
        """
        Stage and commit changes to git.
        
        Returns:
            (success, output_message)
        """
        try:
            # Stage _posts directory
            result = subprocess.run(
                ['git', 'add', '_posts/'],
                cwd=self.repo_dir,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                return False, f"Git add failed: {result.stderr}"
            
            # Commit changes
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=self.repo_dir,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                if "nothing to commit" in result.stdout:
                    return True, "No changes to commit"
                return False, f"Git commit failed: {result.stderr}"
            
            return True, "Changes committed successfully"
        except Exception as e:
            return False, f"Git error: {str(e)}"
    
    def push_changes(self) -> Tuple[bool, str]:
        """
        Push changes to remote repository via SSH.
        
        Returns:
            (success, output_message)
        """
        try:
            result = subprocess.run(
                ['git', 'push', 'origin', 'main'],
                cwd=self.repo_dir,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                # Try 'master' branch if 'main' fails
                result = subprocess.run(
                    ['git', 'push', 'origin', 'master'],
                    cwd=self.repo_dir,
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                if result.returncode != 0:
                    return False, f"Git push failed: {result.stderr}"
            
            return True, "Changes pushed successfully"
        except Exception as e:
            return False, f"Git error: {str(e)}"


class PostEditorWindow(ctk.CTkToplevel):
    """Window for creating or editing a blog post."""
    
    def __init__(self, parent, post_manager: PostManager, git_manager: GitManager, 
                 post_data: Optional[Dict] = None, on_save_callback=None):
        super().__init__(parent)
        
        self.post_manager = post_manager
        self.git_manager = git_manager
        self.on_save_callback = on_save_callback
        self.is_edit_mode = post_data is not None
        self.original_filename = post_data['filename'] if post_data else None
        
        # Load default author from config
        self.default_author = self._load_default_author()
        
        # Window setup
        title = "Editar Post" if self.is_edit_mode else "Novo Post"
        self.title(title)
        self.geometry("800x700")
        
        # Make window modal
        self.transient(parent)
        self.grab_set()
        
        # Create form
        self._create_form(post_data)
    
    def _load_default_author(self) -> str:
        """Load default author from _config.yml"""
        try:
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    return config.get('author', {}).get('name', 'France Florenzano')
        except:
            pass
        return 'France Florenzano'
    
    def _create_form(self, post_data: Optional[Dict]):
        """Create the form fields."""
        # Main container with padding
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(main_frame)
        scroll_frame.pack(fill="both", expand=True)
        
        # Title
        ctk.CTkLabel(scroll_frame, text="Título *", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        self.title_entry = ctk.CTkEntry(scroll_frame, width=700)
        self.title_entry.pack(fill="x", pady=(0, 15))
        if post_data:
            self.title_entry.insert(0, post_data.get('title', ''))
        
        # Author
        ctk.CTkLabel(scroll_frame, text="Autor *", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        self.author_entry = ctk.CTkEntry(scroll_frame, width=700)
        self.author_entry.pack(fill="x", pady=(0, 15))
        author_value = post_data.get('author', '') if post_data else self.default_author
        self.author_entry.insert(0, author_value)
        
        # Categories
        ctk.CTkLabel(scroll_frame, text="Categorias * (separadas por vírgula)", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        self.categories_entry = ctk.CTkEntry(scroll_frame, width=700)
        self.categories_entry.pack(fill="x", pady=(0, 15))
        if post_data:
            categories = post_data.get('categories', [])
            self.categories_entry.insert(0, ', '.join(categories))
        
        # Excerpt
        ctk.CTkLabel(scroll_frame, text="Resumo *", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        self.excerpt_entry = ctk.CTkEntry(scroll_frame, width=700)
        self.excerpt_entry.pack(fill="x", pady=(0, 15))
        if post_data:
            self.excerpt_entry.insert(0, post_data.get('excerpt', ''))
        
        # Date
        ctk.CTkLabel(scroll_frame, text="Data *", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        self.date_entry = ctk.CTkEntry(scroll_frame, width=700)
        self.date_entry.pack(fill="x", pady=(0, 15))
        if post_data:
            date_value = post_data.get('date', '')
            self.date_entry.insert(0, date_value)
        else:
            # Auto-fill with today's date
            today = datetime.now().strftime('%Y-%m-%d')
            self.date_entry.insert(0, today)
        
        # Content
        ctk.CTkLabel(scroll_frame, text="Conteúdo * (Markdown)", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        self.content_text = ctk.CTkTextbox(scroll_frame, width=700, height=300)
        self.content_text.pack(fill="both", expand=True, pady=(0, 15))
        if post_data:
            self.content_text.insert("1.0", post_data.get('content', ''))
        
        # Buttons frame
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        # Cancel button
        cancel_btn = ctk.CTkButton(button_frame, text="Cancelar", command=self.destroy, fg_color="gray")
        cancel_btn.pack(side="left", padx=(0, 10))
        
        # Send button
        send_btn = ctk.CTkButton(button_frame, text="Enviar", command=self._save_post)
        send_btn.pack(side="right")
    
    def _validate_fields(self) -> bool:
        """Validate that all required fields are filled."""
        if not self.title_entry.get().strip():
            messagebox.showerror("Erro", "O título é obrigatório")
            return False
        
        if not self.author_entry.get().strip():
            messagebox.showerror("Erro", "O autor é obrigatório")
            return False
        
        if not self.categories_entry.get().strip():
            messagebox.showerror("Erro", "As categorias são obrigatórias")
            return False
        
        if not self.excerpt_entry.get().strip():
            messagebox.showerror("Erro", "O resumo é obrigatório")
            return False
        
        if not self.date_entry.get().strip():
            messagebox.showerror("Erro", "A data é obrigatória")
            return False
        
        if not self.content_text.get("1.0", "end-1c").strip():
            messagebox.showerror("Erro", "O conteúdo é obrigatório")
            return False
        
        return True
    
    def _save_post(self):
        """Save the post and push to git."""
        if not self._validate_fields():
            return
        
        try:
            # Collect form data
            title = self.title_entry.get().strip()
            author = self.author_entry.get().strip()
            categories_str = self.categories_entry.get().strip()
            categories = [cat.strip() for cat in categories_str.split(',') if cat.strip()]
            excerpt = self.excerpt_entry.get().strip()
            date = self.date_entry.get().strip()
            content = self.content_text.get("1.0", "end-1c").strip()
            
            # Generate filename
            if self.is_edit_mode and self.original_filename:
                # Keep original filename for edits
                filename = self.original_filename
            else:
                filename = self.post_manager.generate_filename(title, date)
            
            filepath = self.post_manager.posts_dir / filename
            
            # Prepare post data
            post_data = {
                'title': title,
                'date': date,
                'author': author,
                'categories': categories,
                'excerpt': excerpt,
                'content': content
            }
            
            # Write file
            self.post_manager.write_post_file(filepath, post_data)
            
            # Commit and push
            action = "atualizado" if self.is_edit_mode else "criado"
            commit_message = f"Post {action}: {title}"
            
            success, msg = self.git_manager.commit_changes(commit_message)
            if not success:
                messagebox.showwarning("Aviso", f"Post salvo, mas commit falhou: {msg}")
            else:
                success, msg = self.git_manager.push_changes()
                if not success:
                    messagebox.showwarning("Aviso", f"Post salvo e commitado, mas push falhou: {msg}")
                else:
                    messagebox.showinfo("Sucesso", f"Post {action} e enviado com sucesso!")
            
            # Callback to refresh list
            if self.on_save_callback:
                self.on_save_callback()
            
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar post: {str(e)}")


class PostListWindow(ctk.CTk):
    """Main window showing list of posts."""
    
    def __init__(self):
        super().__init__()
        
        self.post_manager = PostManager()
        self.git_manager = GitManager()
        
        # Window setup
        self.title("Gerenciador de Posts - Sapieando")
        self.geometry("900x600")
        
        # Create UI
        self._create_ui()
        
        # Load posts
        self._refresh_posts()
    
    def _create_ui(self):
        """Create the UI components."""
        # Header frame
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(header_frame, text="Posts do Blog", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(side="left", padx=20, pady=15)
        
        add_btn = ctk.CTkButton(header_frame, text="+ Novo Post", command=self._add_post, width=120)
        add_btn.pack(side="right", padx=20, pady=15)
        
        # Posts list frame
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Scrollable frame for posts
        self.posts_scroll = ctk.CTkScrollableFrame(list_frame)
        self.posts_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Status label
        self.status_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=(0, 10))
    
    def _refresh_posts(self):
        """Refresh the posts list."""
        # Clear existing posts
        for widget in self.posts_scroll.winfo_children():
            widget.destroy()
        
        # Load posts
        posts = self.post_manager.list_posts()
        
        if not posts:
            no_posts_label = ctk.CTkLabel(self.posts_scroll, text="Nenhum post encontrado. Clique em 'Novo Post' para criar um.", 
                                         font=ctk.CTkFont(size=14))
            no_posts_label.pack(pady=50)
            self.status_label.configure(text="0 posts encontrados")
            return
        
        # Display posts
        for post in posts:
            self._create_post_item(post)
        
        self.status_label.configure(text=f"{len(posts)} post(s) encontrado(s)")
    
    def _create_post_item(self, post: Dict):
        """Create a post item in the list."""
        post_frame = ctk.CTkFrame(self.posts_scroll)
        post_frame.pack(fill="x", pady=5, padx=5)
        
        # Post info
        info_frame = ctk.CTkFrame(post_frame)
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        title_label = ctk.CTkLabel(info_frame, text=post['title'], font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(anchor="w")
        
        date_label = ctk.CTkLabel(info_frame, text=f"Data: {post['date']}", font=ctk.CTkFont(size=12))
        date_label.pack(anchor="w", pady=(5, 0))
        
        filename_label = ctk.CTkLabel(info_frame, text=f"Arquivo: {post['filename']}", font=ctk.CTkFont(size=11), text_color="gray")
        filename_label.pack(anchor="w", pady=(2, 0))
        
        # Buttons frame
        button_frame = ctk.CTkFrame(post_frame)
        button_frame.pack(side="right", padx=10, pady=10)
        
        edit_btn = ctk.CTkButton(button_frame, text="Editar", command=lambda: self._edit_post(post), width=80)
        edit_btn.pack(pady=5)
        
        delete_btn = ctk.CTkButton(button_frame, text="Excluir", command=lambda: self._delete_post(post), 
                                  fg_color="red", hover_color="darkred", width=80)
        delete_btn.pack(pady=5)
    
    def _add_post(self):
        """Open editor for new post."""
        editor = PostEditorWindow(self, self.post_manager, self.git_manager, 
                                 post_data=None, on_save_callback=self._refresh_posts)
    
    def _edit_post(self, post: Dict):
        """Open editor for existing post."""
        try:
            post_data = self.post_manager.parse_post_file(post['filepath'])
            editor = PostEditorWindow(self, self.post_manager, self.git_manager, 
                                     post_data=post_data, on_save_callback=self._refresh_posts)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar post: {str(e)}")
    
    def _delete_post(self, post: Dict):
        """Delete a post after confirmation."""
        response = messagebox.askyesno("Confirmar Exclusão", 
                                       f"Tem certeza que deseja excluir o post '{post['title']}'?")
        
        if response:
            try:
                self.post_manager.delete_post(post['filepath'])
                
                # Commit deletion
                commit_message = f"Post excluído: {post['title']}"
                success, msg = self.git_manager.commit_changes(commit_message)
                
                if success:
                    success, msg = self.git_manager.push_changes()
                    if success:
                        messagebox.showinfo("Sucesso", "Post excluído e alterações enviadas!")
                    else:
                        messagebox.showwarning("Aviso", f"Post excluído e commitado, mas push falhou: {msg}")
                else:
                    messagebox.showwarning("Aviso", f"Post excluído, mas commit falhou: {msg}")
                
                # Refresh list
                self._refresh_posts()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir post: {str(e)}")


def main():
    """Main entry point."""
    app = PostListWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
