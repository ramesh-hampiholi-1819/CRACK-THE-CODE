import json
import os
import urllib.error
import urllib.request


class ExecutionService:
    @staticmethod
    def execute(language, code, stdin=''):
        api_url = os.environ.get('EXECUTION_SERVICE_URL', '').strip()
        token = os.environ.get('EXECUTION_SERVICE_TOKEN', '').strip()

        if not api_url:
            return {
                'configured': False,
                'status': 'not-configured',
                'output': '',
                'error': 'The execution service is not configured. Set EXECUTION_SERVICE_URL and EXECUTION_SERVICE_TOKEN to enable code execution.',
                'execution_time': 0,
            }

        payload = json.dumps({
            'language': language,
            'code': code,
            'stdin': stdin,
        }).encode('utf-8')

        request = urllib.request.Request(
            api_url,
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}',
            },
            method='POST',
        )

        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                body = response.read().decode('utf-8')
                data = json.loads(body) if body else {}
                return {
                    'configured': True,
                    'status': data.get('status', 'success'),
                    'output': data.get('output', ''),
                    'error': data.get('error', ''),
                    'execution_time': data.get('execution_time', 0),
                }
        except urllib.error.HTTPError as exc:
            return {
                'configured': True,
                'status': 'error',
                'output': '',
                'error': f'HTTP {exc.code}: {exc.reason}',
                'execution_time': 0,
            }
        except (urllib.error.URLError, ValueError, json.JSONDecodeError) as exc:
            return {
                'configured': True,
                'status': 'error',
                'output': '',
                'error': f'Execution service could not be reached: {exc}',
                'execution_time': 0,
            }
