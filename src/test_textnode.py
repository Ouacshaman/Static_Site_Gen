import unittest

from textnode import TextNode, split_nodes_delimiter, split_nodes_images, split_nodes_link


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        node3 = TextNode("Test", "Gone")
        node4 = TextNode("Test", "Gone", None)
        node5 = TextNode("This is text with a `code block` word", "text")
        node6 = TextNode(
            "This is text with an" +
            " ![image](https://storage.googleapis.com/qvault-webapp-d" +
            "ynamic-assets/course_assets/zjjcJKZ.png) and another " +
            "![second image](https://storage." +
            "googleapis.com/qvault-webapp-dynamic-as" +
            "sets/course_assets/3elNhQu.png)",
            "text",
        )
        node7 = TextNode(
            "Oh no [trap](ape.com) what",
            "text"
        )
        self.assertEqual(node, node2)
        self.assertEqual(node.__eq__(node2), True)
        self.assertEqual(node3, node4)
        self.assertTrue(node3 != node)
        self.assertEqual(split_nodes_delimiter([node5], "`", "code"), [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ])
        self.assertEqual(split_nodes_images([node6]), [
            TextNode("This is text with an ", "text"),
            TextNode("image",
                     "image",
                     "https://storage.googleapis.com/qvaul" +
                     "t-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", "text"),
            TextNode(
                "second image", "image", "https://storage." +
                "googleapis.com/qvault-webapp-" +
                "dynamic-assets/course_assets/3elNhQu.png"),
        ])
        self.assertEqual(split_nodes_link([node7]), [TextNode("Oh no ", "text"), TextNode("trap", "link", "ape.com"), TextNode(" what", "text")])

        if __name__ == "__main__":
            unittest.main()
