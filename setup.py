from setuptools import setup, find_packages

setup(
    name="yt-whisper",
    version="0.1.0",
    description="YouTube downloader and subtitle generator using Whisper",
    author="leo",
    author_email="mumuli52@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "yt-dlp",
        "openai-whisper",
    ],
    entry_points={
        "console_scripts": [
            "yt-whisper = yt_whisper.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

