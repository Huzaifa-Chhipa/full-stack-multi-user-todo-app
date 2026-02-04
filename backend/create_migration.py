"""Simple script to create initial migration for the Todo AI Chatbot"""
import subprocess
import os

# Change to backend directory
os.chdir('backend')

# Run alembic revision command to create initial migration
result = subprocess.run([
    'alembic', 'revision', '--autogenerate', '-m', 'Initial migration for Todo AI Chatbot'
], capture_output=True, text=True)

print(f"Return code: {result.returncode}")
print(f"Stdout: {result.stdout}")
print(f"Stderr: {result.stderr}")

if result.returncode == 0:
    print("Migration created successfully!")
else:
    print("Failed to create migration")

    # Let's try with offline mode
    print("\nTrying with offline mode...")
    os.environ['ALEMBIC_OFFLINE'] = '1'
    result2 = subprocess.run([
        'alembic', 'revision', '--autogenerate', '-m', 'Initial migration for Todo AI Chatbot'
    ], capture_output=True, text=True, env={**os.environ, 'ALEMBIC_OFFLINE': '1'})

    print(f"Return code: {result2.returncode}")
    print(f"Stdout: {result2.stdout}")
    print(f"Stderr: {result2.stderr}")