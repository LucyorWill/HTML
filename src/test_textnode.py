import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


if __name__ == "__main__":
    unittest.main()
class TestHTMLNode(unittest.TestCase):
      def test_props_to_html(self):
          node = HTMLNode(props={"href": "https://www.google.com"})
          self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
          node2 = HTMLNode(props=None)
          self.assertEqual(node2.props_to_html(), "")
          node3 = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
          self.assertEqual(node3.props_to_html(), ' href="https://www.google.com" target="_blank"')
class TestLeafNode(unittest.TestCase): 
      def test_leaf_to_html_p(self):
          node = LeafNode("p", "Hello, world!")
          self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
          node2 = LeafNode("i","italic text")
          self.assertEqual(node2.to_html(), "<i>italic text</i>")
          node3 = LeafNode(None, "blank")
          self.assertEqual(node3.to_html(), "blank") 
class TestParentNode(unittest.TestCase):
      def test_to_html_with_children(self):
          child_node = LeafNode("span", "child")
          parent_node = ParentNode("div", [child_node])
          self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

      def test_to_html_with_grandchildren(self):
          grandchild_node = LeafNode("b", "grandchild")
          child_node = ParentNode("span", [grandchild_node])
          parent_node = ParentNode("div", [child_node])
          self.assertEqual(
              parent_node.to_html(),
              "<div><span><b>grandchild</b></span></div>",
          )
          child = LeafNode("span", "child")
          with self.assertRaises(ValueError):
              node = ParentNode(None, [child])
              node.to_html()
          with self.assertRaises(ValueError):
              node = ParentNode("div", None)
              node.to_html()
      def test_bold(self):
          node = TextNode("hello", TextType.BOLD)
          html_node = text_node_to_html_node(node)
          self.assertEqual(html_node.tag, "b")
          self.assertEqual(html_node.value, "hello")
      def test_link(self):
          node = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
          html_node = text_node_to_html_node(node)
          self.assertEqual(html_node.tag, "a")
          self.assertEqual(html_node.value, "Boot.dev")
          self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})
      def test_image(self):
          node = TextNode("src", TextType.IMAGE, "src.png")
          html_node = text_node_to_html_node(node)
          self.assertEqual(html_node.tag, "img")
          self.assertEqual(html_node.value, "")
          self.assertEqual(html_node.props, {"src": "src.png", "alt": "src"})
