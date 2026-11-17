"""Run with: docker compose run --rm --no-deps app python -m unittest discover -s tests -v."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.chunker import chunk_pages
from src.document_loader import load_document


class ComponentTests(unittest.TestCase):
    def test_chunk_overlap(self):
        pages = [{"text": "a b c d e f g", "page": 3}]
        result = chunk_pages(pages, size=4, overlap=2)
        self.assertEqual([item["text"] for item in result], ["a b c d", "c d e f", "e f g"])
        self.assertTrue(all(item["page"] == 3 for item in result))

    def test_reject_invalid_overlap(self):
        with self.assertRaises(ValueError):
            chunk_pages([], 5, 5)

    def test_load_utf8_text(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.txt"
            path.write_text("Vacation days: 25", encoding="utf-8")
            self.assertEqual(load_document(path), [{"text": "Vacation days: 25", "page": 0}])

    def test_reject_unknown_format(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                load_document(Path(directory) / "example.exe")

    @patch("src.embeddings.requests.post")
    def test_embedding_api_request(self, post):
        from src.embeddings import embed_texts
        post.return_value.json.return_value = {"embeddings": [[0.1, 0.2]]}
        result = embed_texts(["hello"])
        self.assertEqual(result, [[0.1, 0.2]])
        self.assertTrue(post.call_args.args[0].endswith("/embed"))

    @patch("src.llm.requests.post")
    def test_chat_api_request(self, post):
        from src.llm import answer_question
        post.return_value.json.return_value = {"message": {"content": "25 days"}}
        self.assertEqual(answer_question("How many days?", "25 days"), "25 days")
        self.assertTrue(post.call_args.args[0].endswith("/chat"))


if __name__ == "__main__":
    unittest.main()
