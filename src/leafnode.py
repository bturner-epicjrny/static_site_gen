from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value:
            if self.tag is None: 
                return self.value
            
            html_str = f"<{self.tag}"
            if self.props:
                html_str += f" {self.props_to_html()}"
            html_str += ">"

            html_str += f"{self.value}"

            html_str += f"</{self.tag}>"
            return html_str

        else:
            raise ValueError
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"
