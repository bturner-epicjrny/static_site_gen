class HTMLNode(): 
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value 
        self.children = children 
        self.props = props 

    def to_html(self):
        raise NotImplemented
    
    def props_to_html(self):
        if self.props:
            formatted_str = ""
            for i, (key, value) in enumerate(self.props.items(), start=1):
                formatted_str += f'{key}="{value}"'
                if i < len(self.props):
                    formatted_str += " "
            return formatted_str

        return None  # if self.props is empty or None

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
