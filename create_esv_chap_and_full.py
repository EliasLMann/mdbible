import json
import re
import os

# 1. Ensure the "ESV" directory exists
if not os.path.exists("ESV"):
    os.mkdir("ESV")

# 2. Load ESV JSON data
with open("json/ESV.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    books = data["books"]

book_index = 1
for book_key in books:
    # Convert something like "I_John" -> "I John"
    clean_book_title = book_key.replace("_", " ")
    
    # Build the directory name like "01_Genesis", "02_Exodus", etc.
    indexed_book_title = f"{book_index:02d}_{clean_book_title}"
    
    # Create that directory inside "ESV" if not already there
    book_dir = os.path.join("ESV", indexed_book_title)
    if not os.path.exists(book_dir):
        os.mkdir(book_dir)

    # Get the list of chapters for this book
    book_chapters = books[book_key]  # Each element is a list of verses
    # We'll store them here, to also build the "full" file later
    all_chapters_text = []

    # 4. Create *per-chapter* files
    for chapter_num, chapter_data in enumerate(book_chapters, start=1):
        # Flatten text for each verse in this chapter
        verses = []
        for verse_data in chapter_data:
            verse_text = " ".join(
                chunk[0] for chunk in verse_data if not isinstance(chunk[0], list)
            )
            # Remove awkward spaces before punctuation
            verse_text = re.sub(r'\s([?.,;!"](?:\s|$))', r'\1', verse_text)
            verses.append(verse_text)

        # Write them to a single chapter file, e.g. "Genesis 01.md"
        chapter_filename = f"{clean_book_title} {chapter_num:02d}.md"
        chapter_filepath = os.path.join(book_dir, chapter_filename)

        with open(chapter_filepath, "w", encoding="utf-8") as chapter_file:
            # Title line (no zero-padding in the heading)
            chapter_file.write(f"{clean_book_title} {chapter_num}\n\n")
            # Each verse: "1    text"
            for i, vtext in enumerate(verses, start=1):
                chapter_file.write(f"{i}\t{vtext}\n")
            chapter_file.write("\n")

        # Also prepare data for the "full" file
        all_chapters_text.append(verses)

    # 5. Create the "full" single file: e.g. "Genesis (Full).md"
    #    The "(" helps ensure it sorts before "Genesis 01.md"
    full_book_filename = f"{clean_book_title} (Full).md"
    full_book_filepath = os.path.join(book_dir, full_book_filename)
    
    with open(full_book_filepath, "w", encoding="utf-8") as full_file:
        # First line: just the book name
        full_file.write(f"{clean_book_title}\n\n")
        
        # Then each chapter preceded by a TAB and "Chapter X"
        for chapter_index, verses in enumerate(all_chapters_text, start=1):
            full_file.write(f"\tChapter {chapter_index}\n\n")
            # Each verse: "1    text"
            for verse_num, verse_text in enumerate(verses, start=1):
                full_file.write(f"{verse_num}\t{verse_text}\n")
            full_file.write("\n")

    # Move on to the next book
    book_index += 1
