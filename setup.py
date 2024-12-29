from setuptools import setup, find_packages

setup(
    name="agentic_ideation",
    version="0.1.0",
    description="A framework for AI-driven task generation and execution",
    author="Codeium",
    packages=find_packages(),
    package_dir={"": "src"},
    install_requires=[
        "pydantic>=2.0.0",
        "httpx>=0.24.0",
        "pyyaml>=6.0.0"
    ],
    python_requires=">=3.9",
)
