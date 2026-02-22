from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props) 


    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is required")
        
        if self.children is None:
            raise ValueError("children is required")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        props_html = self.props_to_html()
        if props_html:
            return f"<{self.tag} {props_html}>{children_html}</{self.tag}>"

        return f"<{self.tag}>{children_html}</{self.tag}>"
    