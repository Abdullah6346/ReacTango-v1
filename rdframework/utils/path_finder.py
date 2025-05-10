import os

class PathFinder:
    def find_project_root(self, start_dir):
        """Find the project root directory by looking for frontend/ and backend/ subdirs."""
        current_dir = os.path.abspath(start_dir)
        while True:
            if os.path.exists(os.path.join(current_dir, "frontend")) and \
               os.path.exists(os.path.join(current_dir, "backend")):
                return current_dir
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:  # Reached root
                return None
            current_dir = parent_dir

    def find_components_dir(self, start_dir):
        """Find the components directory (heuristic)."""
        project_root = self.find_project_root(start_dir)
        if project_root:
            components_dir = os.path.join(project_root, "frontend", "app", "components")
            if os.path.isdir(components_dir):
                return components_dir
        # Fallback search (less reliable)
        for root, dirs, _ in os.walk(start_dir):
            if "components" in dirs:
                potential_dir = os.path.join(root, "components")
                # Check if it looks like a React app structure nearby
                if os.path.exists(os.path.join(os.path.dirname(potential_dir), "main.tsx")):
                    return potential_dir
        return None

    def find_backend_dir(self, start_dir):
        """Find the backend directory (heuristic)."""
        project_root = self.find_project_root(start_dir)
        if project_root:
            backend_dir = os.path.join(project_root, "backend")
            if os.path.isdir(backend_dir) and os.path.exists(os.path.join(backend_dir, "manage.py")):
                return backend_dir
        # Fallback: check current dir
        if os.path.exists(os.path.join(start_dir, "manage.py")):
            # Check if it's inside a likely project root
            parent = os.path.dirname(start_dir)
            if os.path.exists(os.path.join(parent, "frontend")):
                return start_dir
        return None 