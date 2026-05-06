import json
import os
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def vite_entry():
    """
    Load Vite entry point for development or production.
    In development (DEBUG=True), uses Vite dev server at http://localhost:5173
    In production, loads compiled assets from manifest.json
    """
    if settings.DEBUG:
        return mark_safe(
            '<script type="module" src="http://localhost:5173/@vite/client"></script>'
            '<script type="module" src="http://localhost:5173/src/main.ts"></script>'
        )
    else:
        # In production, read manifest and load compiled files
        manifest_path = os.path.join(settings.BASE_DIR, 'static', 'dist', 'manifest.json')
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
                entry = manifest.get('src/main.ts', {})
                js_file = entry.get('file', '')
                css_files = entry.get('css', [])
                
                tags = ''
                if css_files:
                    for css_file in css_files:
                        tags += f'<link rel="stylesheet" href="/static/dist/{css_file}">\n'
                if js_file:
                    tags += f'<script type="module" src="/static/dist/{js_file}"></script>'
                
                return mark_safe(tags)
        except (FileNotFoundError, json.JSONDecodeError):
            return mark_safe('')

@register.simple_tag
def vite_asset(asset_name):
    """
    Get the correct path for a Vite asset (in production, resolves from manifest)
    """
    if settings.DEBUG:
        return f'http://localhost:5173/{asset_name}'
    else:
        manifest_path = os.path.join(settings.BASE_DIR, 'static', 'dist', 'manifest.json')
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
                if asset_name in manifest:
                    return f'/static/dist/{manifest[asset_name]["file"]}'
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return f'/static/{asset_name}'
