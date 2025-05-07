# Recipe Processing Project

This is a personal project of mine which takes a url of a youtube recipe video, and generates an output pdf with LaTeX.

Takes a youtube cooking video and turns it into a recipe .pdf document

# Components

## 1. YouTube URL to transcription

1. Take the transcription from the video if it exists
2. If it doesn't, donwload and transcribe it.

## 2. Transcription Parsing

1. Parse the transcription with an LLM and generate the sections from it.
    - Ingredients, unit
    - Preparation required before cooking
    - Recipe Instructions
    
## 3. Document Formatting

1. Take the recipe sections and place them into a LaTeX format 
    - Convert the units to grams with a lookup table
 