from BookGen import BookGen

if __name__ == "__main__":
    book_gen = BookGen()
    sample_title = "The Future of Artificial Intelligence"
    sample_notes = (
        "Explore the advancements in AI technology, its applications across various industries, "
        "ethical considerations, and potential future developments."
    )
    outline = book_gen.generate_outline(sample_title, sample_notes)
    book_gen.save_book_and_outline(sample_title, sample_notes, outline)
    print(book_gen.get_book_and_outline(sample_title))
    book_gen.generate_heading_content(
        sample_title,
        starting_heading_number=1,
    )
    print(book_gen.get_book_and_outline(sample_title))
    book_gen.book_gen(sample_title, "output.docx")
