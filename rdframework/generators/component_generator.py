import os
from ..utils.path_finder import PathFinder
from ..templates.react_templates import ReactTemplates

class ComponentGenerator:
    def __init__(self):
        self.path_finder = PathFinder()
        self.templates = ReactTemplates()

    def generate_component(self, name, component_type="functional"):
        """Generate a new React component"""
        # Find the components directory
        components_dir = self.path_finder.find_components_dir(os.getcwd())
        if not components_dir:
            print("Error: Could not find components directory")
            return False

        # Create component directory
        component_dir = os.path.join(components_dir, name)
        os.makedirs(component_dir, exist_ok=True)

        # Generate component files
        with open(os.path.join(component_dir, f"{name}.tsx"), "w") as f:
            if component_type == "functional":
                f.write(self.templates.get_functional_component_content(name))
            else:
                f.write(self.templates.get_class_component_content(name))

        with open(os.path.join(component_dir, f"{name}.css"), "w") as f:
            f.write(self.templates.get_component_css_content(name))

        with open(os.path.join(component_dir, "index.ts"), "w") as f:
            f.write(self.templates.get_component_index_content(name))

        print(f"Generated {component_type} component: {name}")
        return True 