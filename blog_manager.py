#!/usr/bin/env python3
"""
Blog Post Manager Web Application
Manages Jekyll blog posts through a simple web interface.
Works on any OS with a web browser.
"""

import os
import re
import subprocess
import sys
import threading
import signal
import time
import random
import string
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'blog-manager-secret-key-change-in-production'

# Enable CORS for API endpoints
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Global variable to store the server instance for graceful shutdown
server_instance = None

# Get the workspace directory
WORKSPACE_DIR = Path(__file__).parent.absolute()
POSTS_DIR = WORKSPACE_DIR / "_posts"
CONFIG_FILE = WORKSPACE_DIR / "_config.yml"
COMMENTS_DIR = WORKSPACE_DIR / "_data" / "comments"


class PostManager:
    """Manages blog post file operations including parsing, writing, listing, and deletion.

    This class handles all interactions with markdown post files in the Jekyll _posts/
    directory. It provides methods to parse front matter, generate filenames following
    Jekyll conventions, write posts with properly formatted YAML front matter, list
    all posts, and delete posts.

    Attributes:
        posts_dir (Path): Directory containing post files (default: _posts/).
    """

    def __init__(self, posts_dir: Path = POSTS_DIR):
        """Initialize PostManager with the posts directory.

        Args:
            posts_dir (Path, optional): Directory containing post files.
                Defaults to POSTS_DIR (_posts/).
        """
        self.posts_dir = posts_dir
        self.posts_dir.mkdir(exist_ok=True)

    def parse_post_file(self, filepath: Path) -> Dict:
        """Parse a markdown post file and extract front matter and content.

        Extracts YAML front matter (title, date, author, categories, excerpt) and
        the markdown content body from a Jekyll post file. The file must start with
        '---' and contain valid YAML front matter.

        Args:
            filepath (Path): Path to the markdown post file to parse.

        Returns:
            Dict: Dictionary containing:
                - title (str): Post title
                - date (str): Post date in YYYY-MM-DD format
                - author (str): Post author name
                - categories (List[str]): List of category strings
                - excerpt (str): Brief post description
                - content (str): Markdown content body (without front matter)
                - filename (str): Name of the file
            None: If parsing fails (invalid format, missing front matter, or YAML errors).
        """
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
        """Generate a Jekyll-compliant filename from title and date.

        Creates a filename following Jekyll's YYYY-MM-DD-title.md convention.
        The title is slugified: converted to lowercase, special characters removed,
        and spaces replaced with hyphens.

        Args:
            title (str): Post title to slugify.
            date (str): Post date in YYYY-MM-DD format.

        Returns:
            str: Filename in format YYYY-MM-DD-slugified-title.md.
                If date parsing fails, uses current date.
        """
        # Date normalization: Parse and reformat to ensure YYYY-MM-DD format
        # This handles various date input formats and normalizes them to Jekyll's expected format
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            date_str = date_obj.strftime('%Y-%m-%d')
        except:
            # Fallback to current date if parsing fails
            date_str = datetime.now().strftime('%Y-%m-%d')

        # Slugification process: Convert title to URL-friendly format
        # Step 1: Convert to lowercase and remove special characters (keep word chars, spaces, hyphens)
        # Example: "Hello, World!" -> "hello world"
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        
        # Step 2: Replace multiple spaces or hyphens with a single hyphen
        # Example: "hello  world" -> "hello-world"
        slug = re.sub(r'[-\s]+', '-', slug)
        
        # Step 3: Remove leading/trailing hyphens
        # Example: "-hello-world-" -> "hello-world"
        slug = slug.strip('-')

        return f"{date_str}-{slug}.md"

    def write_post_file(self, filename: str, title: str, author: str,
                       categories: List[str], excerpt: str, date: str, content: str):
        """Write a post file with YAML front matter matching Jekyll format.

        Creates a markdown file with properly formatted YAML front matter followed
        by the content body. Front matter format follows Jekyll conventions:
        - title, author, excerpt: quoted strings
        - date: unquoted YYYY-MM-DD format
        - categories: YAML array format ["Cat1", "Cat2"]

        Args:
            filename (str): Name of the file to write (e.g., 2024-01-01-title.md).
            title (str): Post title (will be quoted in front matter).
            author (str): Post author name (will be quoted in front matter).
            categories (List[str]): List of category strings (formatted as YAML array).
            excerpt (str): Brief post description (will be quoted in front matter).
            date (str): Post date in YYYY-MM-DD format (unquoted in front matter).
            content (str): Markdown content body.
        """
        filepath = self.posts_dir / filename

        # Date normalization: Ensure YYYY-MM-DD format for Jekyll compatibility
        # Jekyll expects dates in this specific format for proper sorting and URL generation
        try:
            # Parse and reformat date to ensure consistency
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            date_str = date_obj.strftime('%Y-%m-%d')
        except:
            date_str = date  # Use as-is if parsing fails

        # Front matter formatting: Jekyll requires specific YAML format for proper parsing
        # 
        # Quoting rules (critical for Jekyll compatibility):
        # - Strings with special chars (title, author, excerpt): MUST be quoted to prevent YAML parsing errors
        # - Date: MUST be unquoted so Jekyll treats it as a date object (not a string)
        # - Categories: MUST be formatted as YAML array ["Cat1", "Cat2"] for proper taxonomy
        #
        # Example front matter:
        # ---
        # title: "My Post Title"      <- Quoted string
        # date: 2024-01-01             <- Unquoted date
        # author: "John Doe"           <- Quoted string
        # categories: ["Tech", "Blog"] <- YAML array with quoted elements
        # excerpt: "Brief description" <- Quoted string
        # ---
        categories_str = '[' + ', '.join([f'"{cat}"' for cat in categories]) + ']'

        front_matter_lines = [
            '---',
            f'title: "{title}"',          # Quoted to handle special characters
            f'date: {date_str}',           # Unquoted for Jekyll date processing
            f'author: "{author}"',         # Quoted to handle special characters
            f'categories: {categories_str}', # YAML array format for taxonomy
            f'excerpt: "{excerpt}"',       # Quoted to handle special characters
            '---'
        ]

        # File structure: Front matter + blank line + content
        # The blank line after front matter is required by Jekyll to separate metadata from content
        file_content = '\n'.join(front_matter_lines) + '\n\n' + content + '\n'

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(file_content)

    def list_posts(self) -> List[Dict]:
        """List all posts in reverse chronological order.

        Scans the posts directory for all .md files, parses each one, and returns
        them sorted by filename (which includes the date) in reverse order (newest first).

        Returns:
            List[Dict]: List of post dictionaries (see parse_post_file for structure).
                Only includes posts that parse successfully. Empty list if no valid posts.
        """
        posts = []
        for filepath in sorted(self.posts_dir.glob('*.md'), reverse=True):
            post = self.parse_post_file(filepath)
            if post:
                posts.append(post)
        return posts

    def delete_post(self, filename: str) -> bool:
        """Delete a post file from the posts directory.

        Args:
            filename (str): Name of the file to delete (e.g., 2024-01-01-title.md).

        Returns:
            bool: True if file was successfully deleted, False if file doesn't exist.
        """
        filepath = self.posts_dir / filename
        if filepath.exists():
            filepath.unlink()
            return True
        return False


class GitManager:
    """Manages git version control operations for blog posts.

    This class handles staging, committing, and pushing changes to the git repository.
    It specifically manages the _posts/ directory and provides methods for committing
    changes with descriptive messages and pushing to the remote repository.

    Attributes:
        workspace_dir (Path): Root directory of the git repository.
    """

    def __init__(self, workspace_dir: Path = WORKSPACE_DIR):
        """Initialize GitManager with the workspace directory.

        Args:
            workspace_dir (Path, optional): Root directory of the git repository.
                Defaults to WORKSPACE_DIR (parent directory of this script).
        """
        self.workspace_dir = workspace_dir

    def commit_changes(self, message: str) -> bool:
        """Stage _posts/ directory and commit changes with the given message.

        Executes:
            1. git add _posts/
            2. git commit -m "{message}"

        Args:
            message (str): Commit message describing the changes.

        Returns:
            bool: True if both staging and commit succeed, False if either fails
                (e.g., no changes to commit, git errors, or conflicts).
        """
        try:
            # Git operation flow - Step 1: Stage changes
            # Add all files in _posts/ directory to the staging area
            # This includes new files, modified files, and deleted files
            subprocess.run(
                ['git', 'add', '_posts/'],
                cwd=self.workspace_dir,
                check=True,
                capture_output=True
            )
            
            # Git operation flow - Step 2: Commit staged changes
            # Create a commit with the provided message
            # This will fail if there are no changes to commit (which is caught below)
            subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=self.workspace_dir,
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            # Commit can fail for several reasons:
            # - No changes to commit (nothing was modified)
            # - Git configuration issues (user.name/user.email not set)
            # - Repository conflicts or errors
            return False

    def push_changes(self) -> bool:
        """Push committed changes to the remote repository.

        Executes:
            git push

        Returns:
            bool: True if push succeeds, False if push fails
                (e.g., network errors, authentication issues, or conflicts).
        """
        try:
            # Git operation flow - Step 3: Push to remote
            # Upload local commits to the remote repository (typically GitHub)
            # This triggers GitHub Pages to rebuild and deploy the site
            subprocess.run(
                ['git', 'push'],
                cwd=self.workspace_dir,
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            # Push can fail for several reasons:
            # - Network connectivity issues
            # - Authentication failures (invalid credentials, SSH key issues)
            # - Remote conflicts (remote has changes not present locally)
            # - Permission issues (no write access to repository)
            return False


class CommentManager:
    """Manages comment file operations and business logic.
    
    This class handles all interactions with comment YAML files in the _data/comments/
    directory. It provides methods to submit comments, list/filter comments, approve/
    reject/delete comments, and validate comment data.
    
    Attributes:
        comments_dir (Path): Directory containing comment files (default: _data/comments/).
        posts_dir (Path): Directory containing post files for title lookup.
    """
    
    def __init__(self, comments_dir: Path = COMMENTS_DIR, posts_dir: Path = POSTS_DIR):
        """Initialize CommentManager with the comments directory.
        
        Args:
            comments_dir (Path, optional): Directory containing comment files.
                Defaults to COMMENTS_DIR (_data/comments/).
            posts_dir (Path, optional): Directory containing post files.
                Defaults to POSTS_DIR (_posts/).
        """
        self.comments_dir = comments_dir
        self.posts_dir = posts_dir
        self.comments_dir.mkdir(parents=True, exist_ok=True)
    
    def submit_comment(self, post_slug: str, name: str, email: str, comment: str) -> Dict:
        """Create a new comment with pending status.
        
        Args:
            post_slug: URL-friendly post identifier
            name: Commenter name (required)
            email: Commenter email (optional)
            comment: Comment text (required, min 10 chars)
        
        Returns:
            Dict with keys: success (bool), message (str), comment_id (str)
        """
        # Validate input
        is_valid, error_msg = self.validate_comment(name, email, comment)
        if not is_valid:
            return {'success': False, 'message': error_msg}
        
        # Generate unique comment ID
        comment_id = self.generate_comment_id()
        
        # Create comment data
        comment_data = {
            'id': comment_id,
            'name': name.strip(),
            'email': email.strip(),
            'comment': comment.strip(),
            'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'status': 'pending',
            'post_slug': post_slug
        }
        
        # Load existing comments for this post
        filepath = self.comments_dir / f"{post_slug}.yml"
        comments = []
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        comments = yaml.safe_load(content) or []
                        if not isinstance(comments, list):
                            comments = []
            except:
                comments = []
        
        # Add new comment
        comments.append(comment_data)
        
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(comments, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
        return {
            'success': True,
            'message': 'Comentário enviado com sucesso! Aguardando aprovação.',
            'comment_id': comment_id
        }
    
    def list_comments(self, status: Optional[str] = None, post_slug: Optional[str] = None) -> List[Dict]:
        """List comments with optional filtering.
        
        Args:
            status: Filter by status (pending/approved/rejected), None for all
            post_slug: Filter by post, None for all posts
        
        Returns:
            List of comment dictionaries sorted by timestamp (newest first)
        """
        all_comments = []
        
        # Determine which files to read
        if post_slug:
            files = [self.comments_dir / f"{post_slug}.yml"]
        else:
            files = list(self.comments_dir.glob('*.yml'))
        
        # Read comments from files
        for filepath in files:
            if not filepath.exists():
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        comments = yaml.safe_load(content) or []
                        if isinstance(comments, list):
                            for comment in comments:
                                if isinstance(comment, dict) and all(k in comment for k in ['id', 'name', 'comment', 'timestamp', 'status', 'post_slug']):
                                    # Add post title for display
                                    comment['post_title'] = self.get_post_title(comment['post_slug'])
                                    all_comments.append(comment)
            except:
                continue
        
        # Filter by status if specified
        if status:
            all_comments = [c for c in all_comments if c.get('status') == status]
        
        # Sort by timestamp (newest first)
        all_comments.sort(key=lambda c: c.get('timestamp', ''), reverse=True)
        
        return all_comments
    
    def get_comment(self, comment_id: str) -> Optional[Dict]:
        """Retrieve a specific comment by ID.
        
        Args:
            comment_id: Unique comment identifier
        
        Returns:
            Comment dictionary or None if not found
        """
        all_comments = self.list_comments()
        for comment in all_comments:
            if comment.get('id') == comment_id:
                return comment
        return None
    
    def approve_comment(self, comment_id: str) -> bool:
        """Update comment status to approved.
        
        Args:
            comment_id: Unique comment identifier
        
        Returns:
            True if successful, False if comment not found
        """
        return self._update_comment_status(comment_id, 'approved')
    
    def reject_comment(self, comment_id: str) -> bool:
        """Update comment status to rejected.
        
        Args:
            comment_id: Unique comment identifier
        
        Returns:
            True if successful, False if comment not found
        """
        return self._update_comment_status(comment_id, 'rejected')
    
    def delete_comment(self, comment_id: str) -> bool:
        """Remove a comment from the comment file.
        
        Args:
            comment_id: Unique comment identifier
        
        Returns:
            True if successful, False if comment not found
        """
        # Find the comment and its file
        for filepath in self.comments_dir.glob('*.yml'):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:
                        continue
                    comments = yaml.safe_load(content) or []
                    if not isinstance(comments, list):
                        continue
                
                # Find and remove the comment
                original_len = len(comments)
                comments = [c for c in comments if c.get('id') != comment_id]
                
                if len(comments) < original_len:
                    # Comment was found and removed
                    with open(filepath, 'w', encoding='utf-8') as f:
                        if comments:
                            yaml.dump(comments, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
                        else:
                            f.write('')  # Empty file if no comments left
                    return True
            except:
                continue
        
        return False
    
    def _update_comment_status(self, comment_id: str, new_status: str) -> bool:
        """Update the status of a comment.
        
        Args:
            comment_id: Unique comment identifier
            new_status: New status value (approved/rejected)
        
        Returns:
            True if successful, False if comment not found
        """
        # Find the comment and its file
        for filepath in self.comments_dir.glob('*.yml'):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:
                        continue
                    comments = yaml.safe_load(content) or []
                    if not isinstance(comments, list):
                        continue
                
                # Find and update the comment
                found = False
                for comment in comments:
                    if comment.get('id') == comment_id:
                        comment['status'] = new_status
                        found = True
                        break
                
                if found:
                    # Write back to file
                    with open(filepath, 'w', encoding='utf-8') as f:
                        yaml.dump(comments, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
                    return True
            except:
                continue
        
        return False
    
    def generate_comment_id(self) -> str:
        """Generate a unique comment ID.
        
        Uses timestamp (milliseconds) + random 6-character alphanumeric suffix.
        Format: {timestamp_ms}_{random}
        Example: 1707318245123_a7k9m2
        
        Returns:
            Unique comment ID string
        """
        timestamp_ms = int(time.time() * 1000)
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"{timestamp_ms}_{random_suffix}"
    
    def validate_comment(self, name: str, email: str, comment: str) -> Tuple[bool, str]:
        """Validate comment submission data.
        
        Validation rules:
        - name: non-empty, trimmed
        - email: valid format if provided, optional
        - comment: minimum 10 characters, trimmed
        
        Args:
            name: Commenter name
            email: Commenter email (can be empty)
            comment: Comment text
        
        Returns:
            (is_valid: bool, error_message: str)
        """
        # Validate name
        if not name or not name.strip():
            return False, "Nome é obrigatório"
        
        # Validate comment length
        if not comment or len(comment.strip()) < 10:
            return False, "O comentário deve ter no mínimo 10 caracteres"
        
        # Validate email format if provided
        if email and email.strip():
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email.strip()):
                return False, "Email inválido"
        
        return True, ""
    
    def get_post_title(self, post_slug: str) -> str:
        """Get post title from post slug for display in moderation interface.
        
        Args:
            post_slug: URL-friendly post identifier
        
        Returns:
            Post title or post_slug if post not found
        """
        # Try to find the post file
        post_files = list(self.posts_dir.glob(f"*{post_slug}*.md"))
        if not post_files:
            return post_slug
        
        # Parse the first matching post
        try:
            with open(post_files[0], 'r', encoding='utf-8') as f:
                content = f.read()
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        front_matter = yaml.safe_load(parts[1])
                        return front_matter.get('title', post_slug)
        except:
            pass
        
        return post_slug


class RateLimiter:
    """Prevent comment spam by limiting submission frequency per IP.
    
    This class tracks comment submissions by IP address and enforces a rate limit
    to prevent automated spam. It maintains an in-memory record of submission
    timestamps and automatically cleans up old entries.
    
    Attributes:
        submissions: Dict mapping IP addresses to lists of submission timestamps
        max_submissions: Maximum submissions per time window (default: 3)
        time_window: Time window in seconds (default: 3600 = 1 hour)
    """
    
    def __init__(self, max_submissions: int = 3, time_window: int = 3600):
        """Initialize RateLimiter with submission limits.
        
        Args:
            max_submissions: Maximum submissions per time window (default: 3)
            time_window: Time window in seconds (default: 3600 = 1 hour)
        """
        self.submissions = {}
        self.max_submissions = max_submissions
        self.time_window = time_window
    
    def check_rate_limit(self, ip_address: str) -> Tuple[bool, str]:
        """Check if IP address has exceeded rate limit.
        
        Args:
            ip_address: Client IP address
        
        Returns:
            (is_allowed: bool, message: str)
            - (True, "") if allowed
            - (False, "Rate limit exceeded") if blocked
        """
        # Clean up old entries first
        self.cleanup_old_entries()
        
        # Get submissions for this IP
        ip_submissions = self.submissions.get(ip_address, [])
        
        # Count submissions within time window
        current_time = time.time()
        recent_submissions = [ts for ts in ip_submissions if current_time - ts < self.time_window]
        
        if len(recent_submissions) >= self.max_submissions:
            return False, "Você atingiu o limite de comentários. Tente novamente mais tarde."
        
        return True, ""
    
    def record_submission(self, ip_address: str):
        """Record a comment submission for rate limiting.
        
        Args:
            ip_address: Client IP address
        """
        current_time = time.time()
        if ip_address not in self.submissions:
            self.submissions[ip_address] = []
        self.submissions[ip_address].append(current_time)
    
    def cleanup_old_entries(self):
        """Remove submission records older than time window.
        
        Called periodically to prevent memory growth.
        """
        current_time = time.time()
        for ip_address in list(self.submissions.keys()):
            self.submissions[ip_address] = [
                ts for ts in self.submissions[ip_address]
                if current_time - ts < self.time_window
            ]
            # Remove IP if no recent submissions
            if not self.submissions[ip_address]:
                del self.submissions[ip_address]


# Global rate limiter instance
rate_limiter = RateLimiter()


class JekyllManager:
    """Manages Jekyll site build operations.

    This class handles triggering Jekyll builds to regenerate the static site
    after post changes. It checks for Jekyll availability and executes builds
    with appropriate timeouts and error handling.

    Attributes:
        workspace_dir (Path): Root directory of the Jekyll site.
    """

    def __init__(self, workspace_dir: Path = WORKSPACE_DIR):
        """Initialize JekyllManager with the workspace directory.

        Args:
            workspace_dir (Path, optional): Root directory of the Jekyll site.
                Defaults to WORKSPACE_DIR (parent directory of this script).
        """
        self.workspace_dir = workspace_dir

    def build_site(self) -> Tuple[bool, str]:
        """Trigger Jekyll build to regenerate static site pages.

        Executes 'bundle exec jekyll build' to regenerate the site after changes.
        Includes a 60-second timeout to prevent hanging builds.

        Returns:
            Tuple[bool, str]: A tuple containing:
                - success (bool): True if build succeeds, False otherwise.
                - message (str): Success message or error details.

        Possible error conditions:
            - Jekyll/bundle not found
            - Build timeout (>60 seconds)
            - Build errors (invalid markdown, configuration issues, etc.)
        """
        try:
            # Jekyll build process - Step 1: Check if Jekyll is available
            # Verify that the 'bundle' command exists on the system
            # Bundle is Ruby's dependency manager and is required to run Jekyll
            result = subprocess.run(
                ['which', 'bundle'],
                cwd=self.workspace_dir,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return False, "Jekyll não encontrado. Execute 'bundle install' primeiro."

            # Jekyll build process - Step 2: Execute the build
            # 'bundle exec jekyll build' does the following:
            # 1. Reads _config.yml for site configuration
            # 2. Processes all markdown files in _posts/ directory
            # 3. Applies layouts from _layouts/ directory
            # 4. Includes partials from _includes/ directory
            # 5. Copies assets from assets/ directory
            # 6. Generates static HTML files in _site/ directory
            # 7. Creates RSS feed, sitemap, and SEO tags (via plugins)
            #
            # The build is local and separate from GitHub Pages deployment
            # GitHub Pages will run its own build when changes are pushed
            build_result = subprocess.run(
                ['bundle', 'exec', 'jekyll', 'build'],
                cwd=self.workspace_dir,
                capture_output=True,
                text=True,
                timeout=60  # 60 second timeout to prevent hanging on large sites
            )

            if build_result.returncode == 0:
                return True, "Site Jekyll reconstruído com sucesso!"
            else:
                # Capture error details for debugging
                # Common errors: invalid YAML, missing layouts, plugin issues
                error_msg = build_result.stderr[:200] if build_result.stderr else "Erro desconhecido"
                return False, f"Erro ao construir site: {error_msg}"

        except subprocess.TimeoutExpired:
            # Build took longer than 60 seconds - likely an infinite loop or very large site
            return False, "Timeout ao construir site Jekyll"
        except FileNotFoundError:
            # Bundle command not found - Jekyll not installed
            return False, "Jekyll não está instalado. Instale com: gem install bundler && bundle install"
        except Exception as e:
            # Catch-all for unexpected errors
            return False, f"Erro ao construir site: {str(e)}"

    def is_jekyll_available(self) -> bool:
        """Check if Jekyll/bundle is available on the system.

        Returns:
            bool: True if bundle command exists and is executable, False otherwise.
        """
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
    """Load default author name from _config.yml configuration file.

    Reads the Jekyll _config.yml file and extracts the author name from the
    author.name field. Falls back to 'France Florenzano' if the file doesn't
    exist, can't be parsed, or doesn't contain the author field.

    Returns:
        str: Author name from config file, or 'France Florenzano' as fallback.
    """
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
    """Display main page listing all blog posts.

    Renders the index.html template with a table of all posts showing title,
    date, author, and categories. Posts are displayed in reverse chronological
    order (newest first).

    Returns:
        str: Rendered HTML template with posts list.
    """
    post_manager = PostManager()
    posts = post_manager.list_posts()
    return render_template('index.html', posts=posts)


@app.route('/new', methods=['GET', 'POST'])
def new_post():
    """Create a new blog post.

    GET: Displays an empty form with default values (current date, default author).

    POST: Validates form data, creates the post file, triggers Jekyll build,
    commits changes to git, and pushes to remote repository. Displays flash
    messages for success/failure of each operation.

    Form validation ensures all fields (title, author, categories, excerpt,
    date, content) are non-empty. Categories are parsed from comma-separated
    values with whitespace trimming.

    Returns:
        str: Rendered edit.html template (GET) or redirect to index (POST success).
    """
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
    """Edit an existing blog post.

    GET: Displays form pre-filled with existing post data.

    POST: Validates form data, updates the post file (creating new file if date
    changed), triggers Jekyll build, commits changes to git, and pushes to remote.
    If the date changes, the old file is deleted and a new file with the updated
    filename is created.

    Args:
        filename (str): Name of the post file to edit (e.g., 2024-01-01-title.md).

    Returns:
        str: Rendered edit.html template (GET) or redirect to index (POST success).
        Redirects to index with error flash if post not found.
    """
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
    """Delete a blog post.

    Requires confirmation via JavaScript before deletion. Deletes the post file,
    triggers Jekyll build to remove the page, commits changes to git, and pushes
    to remote repository. Displays flash messages for success/failure.

    Args:
        filename (str): Name of the post file to delete (e.g., 2024-01-01-title.md).

    Returns:
        Response: Redirect to index page with appropriate flash messages.
    """
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


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Gracefully shutdown the Flask server.

    Displays a shutdown confirmation page and terminates the server process
    after a 1-second delay. The delay allows the response to be sent to the
    browser before the server stops.

    Returns:
        str: Rendered shutdown.html template confirming server shutdown.
    """
    def shutdown_server():
        # Wait a moment for the response to be sent
        import time
        time.sleep(1)
        # Shutdown Flask gracefully
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            # If werkzeug shutdown is not available, use sys.exit
            import sys
            sys.exit(0)
        else:
            func()

    # Start shutdown in a separate thread
    shutdown_thread = threading.Thread(target=shutdown_server)
    shutdown_thread.daemon = True
    shutdown_thread.start()

    return render_template('shutdown.html')


@app.route('/api/comments/submit', methods=['POST', 'OPTIONS'])
def submit_comment():
    """Submit a new comment from blog post.
    
    CORS enabled for cross-origin requests from GitHub Pages.
    
    Request JSON:
        {
            "post_slug": str,
            "name": str,
            "email": str (optional),
            "comment": str,
            "honeypot": str (should be empty)
        }
    
    Response JSON:
        Success: {"success": true, "message": "Comment submitted", "comment_id": str}
        Error: {"success": false, "message": "Error description"}
    
    Status Codes:
        200: Success
        400: Validation error or rate limit exceeded
        500: Server error
    """
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Dados inválidos'}), 400
        
        post_slug = data.get('post_slug', '').strip()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        comment = data.get('comment', '').strip()
        honeypot = data.get('honeypot', '')
        
        # Check honeypot (silent rejection if filled)
        if honeypot:
            # Bot detected - return success but don't create comment
            return jsonify({
                'success': True,
                'message': 'Comentário enviado com sucesso! Aguardando aprovação.',
                'comment_id': 'spam_detected'
            }), 200
        
        # Check rate limit
        ip_address = request.remote_addr or 'unknown'
        allowed, rate_msg = rate_limiter.check_rate_limit(ip_address)
        if not allowed:
            return jsonify({'success': False, 'message': rate_msg}), 400
        
        # Submit comment
        comment_manager = CommentManager()
        result = comment_manager.submit_comment(post_slug, name, email, comment)
        
        if not result['success']:
            return jsonify(result), 400
        
        # Record submission for rate limiting
        rate_limiter.record_submission(ip_address)
        
        # Commit and push to git
        git_manager = GitManager()
        post_title = comment_manager.get_post_title(post_slug)
        commit_message = f"Novo comentário em: {post_title}"
        if git_manager.commit_changes(commit_message):
            git_manager.push_changes()
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro ao processar comentário. Tente novamente.'
        }), 500


@app.route('/comments', methods=['GET'])
def comments_page():
    """Display comment moderation interface.
    
    Query Parameters:
        status: Filter by status (all/pending/approved/rejected), default: all
        search: Search by post title or commenter name
    
    Template: templates/comments.html
    Context:
        - comments: List[Dict] (filtered comments)
        - status_filter: str (current filter)
        - search_query: str (current search)
        - pending_count: int
        - approved_count: int
        - rejected_count: int
    """
    comment_manager = CommentManager()
    
    # Get filter parameters
    status_filter = request.args.get('status', 'all')
    search_query = request.args.get('search', '').strip()
    
    # Get comments based on filter
    if status_filter == 'all':
        comments = comment_manager.list_comments()
    else:
        comments = comment_manager.list_comments(status=status_filter)
    
    # Apply search filter
    if search_query:
        search_lower = search_query.lower()
        comments = [
            c for c in comments
            if search_lower in c.get('name', '').lower() or
               search_lower in c.get('post_title', '').lower()
        ]
    
    # Get counts for each status
    all_comments = comment_manager.list_comments()
    pending_count = len([c for c in all_comments if c.get('status') == 'pending'])
    approved_count = len([c for c in all_comments if c.get('status') == 'approved'])
    rejected_count = len([c for c in all_comments if c.get('status') == 'rejected'])
    
    return render_template('comments.html',
                         comments=comments,
                         status_filter=status_filter,
                         search_query=search_query,
                         pending_count=pending_count,
                         approved_count=approved_count,
                         rejected_count=rejected_count)


@app.route('/comments/approve/<comment_id>', methods=['POST'])
def approve_comment_route(comment_id):
    """Approve a comment.
    
    Actions:
        1. Update comment status to "approved"
        2. Commit changes with message "Approve comment on: {post_title}"
        3. Push to GitHub
    
    Response:
        Redirect to /comments with flash message
    """
    comment_manager = CommentManager()
    git_manager = GitManager()
    
    # Get comment details before approving
    comment = comment_manager.get_comment(comment_id)
    if not comment:
        flash('Comentário não encontrado', 'error')
        return redirect(url_for('comments_page'))
    
    post_title = comment.get('post_title', comment.get('post_slug', 'post'))
    
    # Approve comment
    if comment_manager.approve_comment(comment_id):
        flash('Comentário aprovado!', 'success')
        
        # Commit and push
        commit_message = f"Aprovar comentário em: {post_title}"
        if git_manager.commit_changes(commit_message):
            git_manager.push_changes()
            flash('Alterações enviadas para o repositório GitHub!', 'success')
        else:
            flash('Comentário aprovado localmente, mas houve um erro ao fazer commit/push no git.', 'warning')
    else:
        flash('Erro ao aprovar comentário', 'error')
    
    return redirect(url_for('comments_page'))


@app.route('/comments/reject/<comment_id>', methods=['POST'])
def reject_comment_route(comment_id):
    """Reject a comment.
    
    Actions:
        1. Update comment status to "rejected"
        2. Commit changes with message "Reject comment on: {post_title}"
        3. Push to GitHub
    
    Response:
        Redirect to /comments with flash message
    """
    comment_manager = CommentManager()
    git_manager = GitManager()
    
    # Get comment details before rejecting
    comment = comment_manager.get_comment(comment_id)
    if not comment:
        flash('Comentário não encontrado', 'error')
        return redirect(url_for('comments_page'))
    
    post_title = comment.get('post_title', comment.get('post_slug', 'post'))
    
    # Reject comment
    if comment_manager.reject_comment(comment_id):
        flash('Comentário rejeitado!', 'success')
        
        # Commit and push
        commit_message = f"Rejeitar comentário em: {post_title}"
        if git_manager.commit_changes(commit_message):
            git_manager.push_changes()
            flash('Alterações enviadas para o repositório GitHub!', 'success')
        else:
            flash('Comentário rejeitado localmente, mas houve um erro ao fazer commit/push no git.', 'warning')
    else:
        flash('Erro ao rejeitar comentário', 'error')
    
    return redirect(url_for('comments_page'))


@app.route('/comments/delete/<comment_id>', methods=['POST'])
def delete_comment_route(comment_id):
    """Delete a comment permanently.
    
    Actions:
        1. Remove comment from file
        2. Commit changes with message "Delete comment: {comment_id}"
        3. Push to GitHub
    
    Response:
        Redirect to /comments with flash message
    """
    comment_manager = CommentManager()
    git_manager = GitManager()
    
    # Get comment details before deleting
    comment = comment_manager.get_comment(comment_id)
    if not comment:
        flash('Comentário não encontrado', 'error')
        return redirect(url_for('comments_page'))
    
    post_title = comment.get('post_title', comment.get('post_slug', 'post'))
    
    # Delete comment
    if comment_manager.delete_comment(comment_id):
        flash('Comentário deletado!', 'success')
        
        # Commit and push
        commit_message = f"Deletar comentário: {comment_id}"
        if git_manager.commit_changes(commit_message):
            git_manager.push_changes()
            flash('Alterações enviadas para o repositório GitHub!', 'success')
        else:
            flash('Comentário deletado localmente, mas houve um erro ao fazer commit/push no git.', 'warning')
    else:
        flash('Erro ao deletar comentário', 'error')
    
    return redirect(url_for('comments_page'))


if __name__ == '__main__':
    jekyll_manager = JekyllManager()
    jekyll_available = jekyll_manager.is_jekyll_available()
    
    print("\n" + "="*60)
    print("Blog Post Manager - Web Interface")
    print("="*60)
    print(f"\nAcesse: http://127.0.0.1:7856")
    
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
    
    # Use a shutdown handler for graceful shutdown
    def signal_handler(sig, frame):
        """Handle SIGTERM and SIGINT signals for graceful shutdown.

        Called when the user presses Ctrl+C or the process receives a termination
        signal. Prints a shutdown message and exits cleanly.

        Args:
            sig: Signal number.
            frame: Current stack frame.
        """
        print('\n\nEncerrando servidor...')
        sys.exit(0)
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        print("\n" + "="*60)
        print("Blog Post Manager - Web Interface")
        print("="*60)
        print(f"\nAcesse: http://127.0.0.1:7856")
        
        jekyll_manager = JekyllManager()
        jekyll_available = jekyll_manager.is_jekyll_available()
        
        if jekyll_available:
            print("\n✓ Jekyll detectado - páginas serão geradas automaticamente")
            print("  Para ver o site localmente, execute em outro terminal:")
            print("  bundle exec jekyll serve")
            print("  Depois acesse: http://localhost:4000")
        else:
            print("\n⚠ Jekyll não encontrado")
            print("  Para gerar páginas localmente, instale Jekyll:")
            print("  gem install bundler && bundle install")
        
        print("\nPressione Ctrl+C ou use o botão 'Fechar' no navegador para parar o servidor\n")
        print("="*60 + "\n")
        
        app.run(debug=True, host='127.0.0.1', port=7856, use_reloader=False)
    except KeyboardInterrupt:
        print('\n\nServidor encerrado pelo usuário.')
        sys.exit(0)
