import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "b", [1, 2, 3])
        node1 = HTMLNode("a", "b", [1, 2, 3], None)
        node2 = HTMLNode("p", None, [3, 4, 4])
        node3 = HTMLNode("p", None, [3, 4, 4], None)
        node4 = HTMLNode()
        node5 = HTMLNode(None, None, None, {'href': 'deez', 1: 2})
        node6 = LeafNode("p", "apple", {'href': '2016'})
        node7 = LeafNode(None, None)
        node8 = LeafNode("h1", "Heading1")
        node9 = LeafNode(None, "raw")
        node10 = LeafNode("a", "link", {'a': 1, 'b': 2, 'c': 3})
        node11 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node4, HTMLNode())
        self.assertEqual(node, node1)
        self.assertEqual(node2, node3)
        self.assertEqual(node5.props_to_html(), "href=\"deez\" 1=\"2\"")
        self.assertEqual(node6.to_html(), "<p href=\"2016\">apple</p>")
        with self.assertRaises(ValueError):
            node7.to_html()
        self.assertEqual(node8.to_html(), "<h1>Heading1</h1>")
        self.assertEqual(node9.to_html(), "raw")
        self.assertEqual(node10.to_html(), "<a a=\"1\" b=\"2\"" +
                                           " c=\"3\">link</a>")
        self.assertEqual(node11.to_html(), "<p><b>Bold text</b>Normal " +
                                           "text<i>italic " +
                                           "text</i>Normal text</p>")


if __name__ == "__main__":
    unittest.main()
