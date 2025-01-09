import json
import re
import os

# Create the ESV directory if it doesn't exist
if not os.path.exists("ESV"):
    os.mkdir("ESV")

# Load the JSON data
with open("json/ESV.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    books = data["books"]

book_index = 1
for book_title in books:
    # Convert something like "I_John" -> "I John"
    clean_book_title = book_title.replace("_", " ")

    # Create a directory name like "01_Genesis"
    indexed_book_title = f"{book_index:02d}_{clean_book_title}"
    
    # Create the directory in "ESV"
    book_dir = os.path.join("ESV", indexed_book_title)
    if not os.path.exists(book_dir):
        os.mkdir(book_dir)
    
    # Get all chapters for this book
    book = books[book_title]
    chapters = list(book)  # Each element in 'chapters' is a list of verses
    
    # For each chapter
    for i, chapter in enumerate(chapters, start=1):
        verses = []
        for verse_data in chapter:
            # Flatten and join the text chunks
            verse_text = " ".join(
                chunk[0] for chunk in verse_data if not isinstance(chunk[0], list)
            )
            # Remove awkward spaces before punctuation
            verse_text = re.sub(r'\s([?.,;!"](?:\s|$))', r'\1', verse_text)
            verses.append(verse_text)
        
        # Zero-padded filename for the chapter: "Genesis 01.md"
        chapter_file_path = os.path.join(
            book_dir,
            f"{clean_book_title} {i:02d}.md"
        )
        
        # Write the file
        with open(chapter_file_path, "w", encoding="utf-8") as f:
            # Heading: "Genesis 1" (no zero padding in the heading)
            f.write(f"{clean_book_title} {i}\n\n")
            
            # Write each verse as `1    text`
            for idx, verse in enumerate(verses, start=1):
                f.write(f"{idx}\t{verse}\n")
            
            f.write("\n")
    
    book_index += 1
