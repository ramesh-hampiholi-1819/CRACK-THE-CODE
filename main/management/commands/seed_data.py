from django.core.management.base import BaseCommand

from accounts.models import UserProfile
from main.models import Challenge, Language, Progress, Submission, Tutorial


class Command(BaseCommand):
    help = 'Seed the database with demo languages, tutorials, and challenges.'

    def handle(self, *args, **options):
        Progress.objects.all().delete()
        Submission.objects.all().delete()
        Challenge.objects.all().delete()
        Tutorial.objects.all().delete()
        Language.objects.all().delete()
        UserProfile.objects.all().delete()

        languages = [
            {
                'name': 'HTML',
                'slug': 'html',
                'tagline': 'Structure the web clearly.',
                'description': 'Learn semantic markup, forms, accessibility, and page structure.',
                'color': '#f97316',
                'is_featured': True,
                'order': 1,
            },
            {
                'name': 'CSS',
                'slug': 'css',
                'tagline': 'Style interfaces with precision.',
                'description': 'Explore layouts, responsive design, colors, and visual hierarchy.',
                'color': '#0ea5e9',
                'is_featured': True,
                'order': 2,
            },
            {
                'name': 'Python',
                'slug': 'python',
                'tagline': 'Write clear, expressive logic.',
                'description': 'Learn Python syntax, loops, functions, and problem solving.',
                'color': '#4f46e5',
                'is_featured': True,
                'order': 3,
            },
            {
                'name': 'Java',
                'slug': 'java',
                'tagline': 'Build object-oriented programs.',
                'description': 'Understand classes, methods, arrays, and structured application design.',
                'color': '#f59e0b',
                'is_featured': False,
                'order': 4,
            },
            {
                'name': 'C',
                'slug': 'c',
                'tagline': 'Master low-level systems thinking.',
                'description': 'Work with variables, pointers, loops, and memory-aware code.',
                'color': '#22c55e',
                'is_featured': False,
                'order': 5,
            },
        ]

        created_languages = {}
        for data in languages:
            language = Language.objects.create(**data)
            created_languages[language.slug] = language

        tutorials = [
            ('html', 'HTML Document Structure', 'html-document-structure', 'Understand the key parts of an HTML file and how semantic elements organize content.', 'HTML documents are built from a declaration, a document head, and a body. Semantic tags like header, main, section, and footer improve accessibility and readability.', 'Beginner', 1),
            ('css', 'CSS Box Model', 'css-box-model', 'Learn padding, margins, borders, and layout flow with practical examples.', 'Every visible element follows the box model. Margins separate elements, borders define edges, and padding creates space inside content areas.', 'Beginner', 1),
            ('python', 'Python Variables and Types', 'python-variables', 'Store information with variables and understand primitive data types.', 'Python variables are dynamically typed, meaning they can hold strings, numbers, or booleans without explicit declarations.', 'Beginner', 1),
            ('java', 'Java Methods', 'java-methods', 'Break logic into reusable methods to keep code readable and organized.', 'Methods let you group behavior into blocks that can be called repeatedly. They make large programs easier to maintain.', 'Intermediate', 1),
            ('c', 'C Input and Output', 'c-input-output', 'Use printf and scanf to communicate with users and read values from the terminal.', 'C programs rely on standard library functions for input and output; proper format specifiers are essential for accurate values.', 'Beginner', 1),
        ]

        for language_slug, title, slug, excerpt, content, difficulty, order in tutorials:
            Tutorial.objects.create(
                language=created_languages[language_slug],
                title=title,
                slug=slug,
                excerpt=excerpt,
                content=content,
                difficulty=difficulty,
                order=order,
            )

        challenges = [
            {
                'language': created_languages['html'],
                'title': 'Build a Hero Banner',
                'slug': 'hero-banner',
                'difficulty': 'Easy',
                'description': 'Create a simple landing section with a heading, supporting text, and a call-to-action button.',
                'instructions': 'Use semantic HTML elements to lay out a hero section. Keep it centered and readable.',
                'starter_code': '<section class="hero">\n  <h1>Learn to build</h1>\n  <p>Practice with clean, readable code.</p>\n  <button>Start now</button>\n</section>',
                'example_input': '',
                'example_output': '',
                'constraints': 'Use only HTML; no external libraries.',
                'hints': 'Use a section, heading, paragraph, and button element.',
                'is_featured': True,
                'expected_output': 'hero',
            },
            {
                'language': created_languages['python'],
                'title': 'Even or Odd',
                'slug': 'even-or-odd',
                'difficulty': 'Easy',
                'description': 'Read a number and print whether it is even or odd.',
                'instructions': 'Take user input and print the result in a clear sentence.',
                'starter_code': 'number = int(input())\n# your code here',
                'example_input': '8\n',
                'example_output': 'Even',
                'constraints': 'Use the input value exactly once and keep output concise.',
                'hints': 'Check the remainder by dividing by 2.',
                'is_featured': True,
                'expected_output': 'Even',
            },
            {
                'language': created_languages['python'],
                'title': 'Sum of First Ten Numbers',
                'slug': 'sum-first-ten',
                'difficulty': 'Medium',
                'description': 'Use a loop to calculate the sum of numbers from 1 to 10.',
                'instructions': 'Write a loop that adds each number and prints the final sum.',
                'starter_code': 'total = 0\nfor value in range(1, 11):\n    total += value\nprint(total)',
                'example_input': '',
                'example_output': '55',
                'constraints': 'No built-in sum function.',
                'hints': 'Incrementally add each value to a running total.',
                'is_featured': False,
                'expected_output': '55',
            },
            {
                'language': created_languages['java'],
                'title': 'Fibonacci Sequence',
                'slug': 'java-fibonacci',
                'difficulty': 'Medium',
                'description': 'Generate the first 10 numbers in the Fibonacci sequence.',
                'instructions': 'Write a Java method that prints the sequence.',
                'starter_code': 'public class Main {\n    public static void main(String[] args) {\n        int a = 0, b = 1;\n        System.out.print(a + " " + b + " ");\n        for (int i = 2; i < 10; i++) {\n            int next = a + b;\n            System.out.print(next + " ");\n            a = b;\n            b = next;\n        }\n    }\n}',
                'example_input': '',
                'example_output': '0 1 1 2 3 5 8 13 21 34',
                'constraints': 'Print values on one line.',
                'hints': 'Use a loop and maintain two previous values.',
                'is_featured': False,
                'expected_output': '0 1 1 2 3 5 8 13 21 34',
            },
            {
                'language': created_languages['c'],
                'title': 'Average of Three Numbers',
                'slug': 'average-three',
                'difficulty': 'Easy',
                'description': 'Take three integers and print their average as a float.',
                'instructions': 'Use scanf to read three values and print the average.',
                'starter_code': '#include <stdio.h>\nint main() {\n    int a, b, c;\n    scanf("%d %d %d", &a, &b, &c);\n    return 0;\n}',
                'example_input': '1 2 3\n',
                'example_output': '2.00',
                'constraints': 'Calculate using floating-point math.',
                'hints': 'Cast to float before dividing.',
                'is_featured': False,
                'expected_output': '2.00',
            },
            {
                'language': created_languages['css'],
                'title': 'Card Layout Practice',
                'slug': 'card-layout-practice',
                'difficulty': 'Medium',
                'description': 'Build a responsive card layout with a title, text, and button.',
                'instructions': 'Use CSS to style cards, align them in a grid, and add a subtle hover effect.',
                'starter_code': '.cards { display: grid; gap: 1rem; }\n.card { padding: 1rem; border-radius: 12px; }',
                'example_input': '',
                'example_output': '',
                'constraints': 'Keep the layout responsive and visually balanced.',
                'hints': 'Use grid and a hover transform for polish.',
                'is_featured': True,
                'expected_output': 'responsive',
            },
        ]

        for challenge_data in challenges:
            Challenge.objects.create(**challenge_data)

        self.stdout.write(self.style.SUCCESS('Seed data created successfully.'))
