from .base_templates import BaseTemplates

class ReactTemplates(BaseTemplates):
    """Templates for React-related files"""

    def get_dockerignore_content(self):
        """Get content for .dockerignore file"""
        return """node_modules
npm-debug.log
dist
.git
.gitignore
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
README.md
"""

    def get_dockerfile_content(self):
        """Get content for Dockerfile"""
        return """FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
"""

    def get_readme_content(self):
        """Get content for README.md"""
        return """# React Frontend

This is the frontend part of the React-Django project, built with:
- React
- TypeScript
- TanStack Router
- Vite
- TailwindCSS

## Development

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start development server:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

## Project Structure

- `app/` - Main application code
  - `routes/` - Route components
  - `components/` - Reusable components
  - `api.ts` - API client configuration
  - `root.tsx` - Root component
  - `routes.ts` - Route definitions
"""

    def get_package_json_content(self, project_name):
        """Get content for package.json"""
        return f"""{{
  "name": "{project_name}-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  }},
  "dependencies": {{
    "@tanstack/react-router": "^1.15.0",
    "@tanstack/react-router-devtools": "^1.15.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0"
  }},
  "devDependencies": {{
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "@vitejs/plugin-react": "^4.0.0",
    "autoprefixer": "^10.4.0",
    "eslint": "^8.0.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.3.0",
    "typescript": "^5.0.0",
    "vite": "^5.0.0"
  }}
}}
"""

    def get_router_config_content(self):
        """Get content for react-router.config.ts"""
        return """import { createRouter } from '@tanstack/react-router'
import { routeTree } from './app/routes'

export const router = createRouter({ routeTree })

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
"""

    def get_tsconfig_content(self):
        """Get content for tsconfig.json"""
        return """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./app/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
"""

    def get_vite_config_content(self):
        """Get content for vite.config.ts"""
        return """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './app'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
"""

    def get_root_tsx_content(self):
        """Get content for root.tsx"""
        return """import { RouterProvider } from '@tanstack/react-router'
import { router } from '../react-router.config'
import './app.css'

function App() {
  return <RouterProvider router={router} />
}

export default App
"""

    def get_routes_ts_content(self):
        """Get content for routes.ts"""
        return """import { createRootRoute, createRoute } from '@tanstack/react-router'
import { Welcome } from './welcome/welcome'

const rootRoute = createRootRoute({
  component: () => (
    <div className="min-h-screen bg-gray-100">
      <Welcome />
    </div>
  ),
})

const homeRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: () => <div>Home</div>,
})

export const routeTree = rootRoute.addChildren([homeRoute])
"""

    def get_app_css_content(self):
        """Get content for app.css"""
        return """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  margin: 0;
  min-width: 320px;
  min-height: 100vh;
}
"""

    def get_api_ts_content(self):
        """Get content for api.ts"""
        return """import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
})

export default api
"""

    def get_home_route_tsx_content(self):
        """Get content for home.tsx"""
        return """import { Link } from '@tanstack/react-router'

export function Home() {
  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
            Welcome to Your App
          </h1>
          <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
            Get started by editing this page.
          </p>
          <div className="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
            <div className="rounded-md shadow">
              <Link
                to="/"
                className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10"
              >
                Get started
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
"""

    def get_welcome_tsx_content(self):
        """Get content for welcome.tsx"""
        return """import { useState } from 'react'
import logoLight from './logo-light.svg'
import logoDark from './logo-dark.svg'

export function Welcome() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center">
          <img
            src={logoLight}
            className="h-24 mx-auto"
            alt="Logo"
          />
          <h1 className="mt-6 text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
            Welcome to Your App
          </h1>
          <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
            Get started by editing this page.
          </p>
          <div className="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
            <div className="rounded-md shadow">
              <button
                onClick={() => setCount((count) => count + 1)}
                className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10"
              >
                Count is {count}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
"""

    def get_logo_light_svg_content(self):
        """Get content for logo-light.svg"""
        return """<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="15" fill="#747bff"/>
  <path fill="#fff" d="M62.5 12.5h-25v12.5h12.5v50h12.5z"/>
  <path fill="#fff" d="M37.5 87.5h25v-12.5h-12.5v-50h-12.5z"/>
</svg>"""

    def get_logo_dark_svg_content(self):
        """Get content for logo-dark.svg"""
        return """<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="15" fill="#1a1a1a"/>
  <path fill="#fff" d="M62.5 12.5h-25v12.5h12.5v50h12.5z"/>
  <path fill="#fff" d="M37.5 87.5h25v-12.5h-12.5v-50h-12.5z"/>
</svg>"""

    def get_functional_component_content(self, name):
        """Get content for functional component"""
        return f"""import {{ useState }} from 'react'
import './{name}.css'

interface {name}Props {{
  // Add your props here
}}

export function {name}({{ }}: {name}Props) {{
  const [state, setState] = useState()

  return (
    <div className="{name.lower()}-container">
    </div>
  )
}}
"""

    def get_class_component_content(self, name):
        """Get content for class component"""
        return f"""import {{ Component }} from 'react'
import './{name}.css'

interface {name}Props {{
  // Add your props here
}}

interface {name}State {{
  // Add your state here
}}

export class {name} extends Component<{name}Props, {name}State> {{
  constructor(props: {name}Props) {{
    super(props)
    this.state = {{
      // Initialize your state here
    }}
  }}

  render() {{
    return (
      <div className="{name.lower()}-container">
      </div>
    )
  }}
}}
"""

    def get_component_css_content(self, name):
        """Get content for component CSS"""
        return f""".{name.lower()}-container {{
  /* Add your styles here */
}}
"""

    def get_component_index_content(self, name):
        """Get content for component index file"""
        return f"""export {{ {name} }} from './{name}'
""" 