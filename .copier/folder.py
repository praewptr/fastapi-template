import yaml

def generate_config(include_frontend):
    config = {
        '_exclude': [
            # Global
            '.vscode',
            '.mypy_cache',
            'poetry.lock',
            # Python
            '__pycache__',
            'app.egg-info',
            '*.pyc',
            '.mypy_cache',
            '.coverage',
            'htmlcov',
            'poetry.lock',
            '.cache',
            '.venv',
            # Conditional Frontend
        ]
    }

    if include_frontend:
        config['_exclude'].append('frontend')

    # Logs
    config['_exclude'].extend([
        'logs',
        '*.log',
        'npm-debug.log*',
        'yarn-debug.log*',
        'yarn-error.log*',
        'pnpm-debug.log*',
        'lerna-debug.log*',
        'node_modules',
        'dist',
        'dist-ssr',
        '*.local'
    ])

    # Editor directories and files
    config['_exclude'].extend([
        '.idea',
        '.DS_Store',
        '*.suo',
        '*.ntvs*',
        '*.njsproj',
        '*.sln',
        '*.sw?'
    ])

    with open('config.yml', 'w') as file:
        yaml.dump(config, file)

# Example usage
include_frontend = True  # Set this based on user input or conditions
generate_config(include_frontend)
