# AI-Powered Blog Platform

A full-stack web application for writing, managing, and publishing blog posts with the help of artificial intelligence.

## Screenshot
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/00096dfe-fec9-4a47-a725-926ab36dae80" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/616d8e90-0d29-4f54-b7fa-7d966baab92b" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/640c21a4-4caf-4a89-8441-abd8b6fb0144" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/dfb598ab-bdb2-4f3f-a2d9-b49a4353a508" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/e3798496-7992-4624-9978-33b6da2d8b3d" />

## Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **React Markdown** - Markdown rendering with live preview
- **React MD Editor** - Advanced Markdown editor component

### Backend
- **FastAPI** - Modern Python web framework
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation using Python type annotations
- **OpenAI API** - AI-powered content generation
- **Python-JOSE** - JWT authentication
- **Passlib** - Password hashing

### Database
- **MongoDB** - NoSQL database for storing blog posts, users, categories, and tags
  - Works with both local MongoDB and MongoDB Atlas

## Features

### AI-Based Content Suggestions
- Users type a broad topic (e.g., "Healthy Morning Habits")
- Application calls OpenAI API to return outline ideas, suggested headings, or draft intros
- Multiple suggestion types: outline, headings, intro

### Markdown Editor with Preview
- Split-pane text editor with live preview
- Write standard Markdown syntax on one side
- See formatted HTML on the other side in real-time
- Supports GitHub Flavored Markdown (GFM)

### SEO Optimization Tools
- Automatic evaluation of blog drafts
- Suggests meta titles and target keywords
- Auto-generate page descriptions
- SEO scoring system with actionable suggestions
- Keyword analysis and content recommendations

### User Authentication
- JWT-based authentication system
- User registration and login
- Protected routes and API endpoints
- Secure password hashing with bcrypt

### Blog Post Management
- Create, read, update, delete (CRUD) operations
- Draft and published states
- Category and tag organization
- Author attribution

## Project Structure

```
intern-pro-2/
├── frontend/                 # Next.js frontend application
│   ├── src/
│   │   ├── app/             # Next.js App Router pages
│   │   │   ├── page.tsx     # Home page
│   │   │   ├── login/       # Login page
│   │   │   ├── register/    # Registration page
│   │   │   ├── dashboard/   # User dashboard
│   │   │   ├── posts/       # Blog post editing
│   │   │   └── demo/        # Demo page
│   │   ├── components/      # React components
│   │   │   ├── MarkdownEditor.tsx
│   │   │   └── SplitMarkdownEditor.tsx
│   │   └── lib/            # Utility functions
│   │       └── api.ts       # API client
│   ├── package.json
│   └── tailwind.config.ts
├── backend/                 # FastAPI backend application
│   ├── main.py             # Application entry point
│   ├── requirements.txt    # Python dependencies
│   ├── .env                # Environment variables
│   ├── models/             # Data models
│   │   ├── database.py     # MongoDB connection
│   │   └── schemas.py      # Pydantic models
│   └── routers/            # API route handlers
│       ├── auth.py         # Authentication endpoints
│       ├── blog_posts.py   # Blog post CRUD
│       ├── ai_features.py  # AI-powered features
│       └── seo_tools.py    # SEO analysis tools
└── README.md              # This file
```

## Setup Instructions

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- MongoDB (local installation or MongoDB Atlas)
- OpenAI API key

### 1. Clone the Repository

```bash
git clone <repository-url>
cd intern-pro-2
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the `backend` directory:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_blog_platform

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini  # Cost-effective small model (default)

# JWT Configuration
SECRET_KEY=your_secret_key_here_change_this_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Note**: The project uses `gpt-4o-mini` by default, which is a small, low-power, cost-effective model. You can change this to other models like `gpt-4o`, `gpt-3.5-turbo`, etc., by modifying the `OPENAI_MODEL` variable.

#### Start MongoDB

You can use either local MongoDB or MongoDB Atlas:

**Option 1: Local MongoDB**
```bash
# On Windows (if installed as service)
# MongoDB should be running automatically

# On macOS with Homebrew
brew services start mongodb-community

# On Linux
sudo systemctl start mongod
```

**Option 2: MongoDB Atlas (Recommended)**
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and create a free account
2. Create a new cluster (free tier is available)
3. Create a database user with read/write permissions
4. Whitelist your IP address (or use 0.0.0.0/0 for development)
5. Get your connection string from the Atlas dashboard
6. Update the `MONGODB_URL` in your `.env` file:

```env
MONGODB_URL=mongodb+srv://iankr347_db_user:<db_password>@cluster0.smqjxtu.mongodb.net/?appName=Cluster0
```

Replace:
- `<db_password>` with your actual database password for the iankr347_db_user user
- Note: Your connection string uses `?appName=Cluster0` which is specific to your cluster configuration

#### Run the Backend Server

```bash
python main.py
```

The backend will be available at `http://localhost:8000`

API documentation (Swagger UI) will be available at `http://localhost:8000/docs`

### 3. Frontend Setup

#### Install Node.js Dependencies

```bash
cd frontend
npm install
```

#### Configure Environment Variables

Create a `.env.local` file in the `frontend` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Run the Frontend Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication

- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

**Note**: Registration is disabled. Use the test account:
- Username: `admin234ai@test.com`
- Password: `12345ty`

### Blog Posts

- `POST /api/blog-posts/` - Create a new blog post
- `GET /api/blog-posts/` - Get all blog posts (with optional filters)
- `GET /api/blog-posts/{post_id}` - Get a specific blog post
- `PUT /api/blog-posts/{post_id}` - Update a blog post
- `DELETE /api/blog-posts/{post_id}` - Delete a blog post
- `POST /api/blog-posts/categories` - Create a category
- `GET /api/blog-posts/categories/` - Get all categories
- `POST /api/blog-posts/tags` - Create a tag
- `GET /api/blog-posts/tags/` - Get all tags

### AI Features

- `POST /api/ai/suggestions` - Get AI content suggestions
- `POST /api/ai/rewrite` - Rewrite text using AI
- `POST /api/ai/generate-outline` - Generate blog post outline

### SEO Tools

- `POST /api/seo/analyze` - Analyze content for SEO
- `POST /api/seo/generate-meta` - Generate meta tags

## Usage

### 1. Register a User Account

Navigate to `http://localhost:3000/register` and create a new account.

### 2. Login

Use your credentials to login at `http://localhost:3000/login`.

### 3. Create a Blog Post

- Go to the dashboard after login
- Click "New Post" to create a new blog post
- Enter title, tags, and content using the Markdown editor
- Use the split-pane view to see live preview
- Save as draft or publish directly

### 4. Use AI Features

- Click "Get AI Suggestions" to get content ideas
- Use "Improve Writing" to enhance your text with AI
- Generate outlines for new topics

### 5. Optimize for SEO

- Click "Analyze SEO" to get SEO score and suggestions
- Review keyword analysis
- Auto-generate meta titles and descriptions
- Implement suggestions to improve search rankings

### 6. Try the Demo

Visit `http://localhost:3000/demo` to try the Markdown editor without registration.

## Development

### Backend Development

The backend uses FastAPI with automatic API documentation. Visit `http://localhost:8000/docs` for interactive API documentation.

### Frontend Development

The frontend uses Next.js 14 with the App Router. Pages are located in `src/app/` directory.

### Adding New Features

1. **Backend**: Add new endpoints in appropriate router files in `backend/routers/`
2. **Frontend**: Create new pages in `frontend/src/app/` and components in `frontend/src/components/`
3. **Database**: Update schemas in `backend/models/schemas.py` if needed

## Security Considerations

- Change the `SECRET_KEY` in the backend `.env` file for production
- Use environment variables for all sensitive configuration
- Implement rate limiting for API endpoints in production
- Add HTTPS/TLS for production deployments
- Regularly update dependencies for security patches

## Deployment

### Backend Deployment

1. Deploy the FastAPI application using a service like:
   - AWS Elastic Beanstalk
   - Google Cloud Run
   - Heroku
   - DigitalOcean App Platform

2. Set up a production MongoDB instance (MongoDB Atlas recommended)

3. Configure production environment variables

### Frontend Deployment

1. Build the Next.js application:
   ```bash
   cd frontend
   npm run build
   ```

2. Deploy the built application to:
   - Vercel (recommended for Next.js)
   - Netlify
   - AWS Amplify
   - Any static hosting service

## Troubleshooting

### MongoDB Connection Issues

**For Local MongoDB:**
- Ensure MongoDB is running
- Check the `MONGODB_URL` in your `.env` file
- Verify MongoDB is accessible on the specified port

**For MongoDB Atlas:**
- Verify your connection string format
- Check that your IP address is whitelisted in Atlas
- Ensure your database user has the correct permissions
- Verify your username and password are correct
- Check that your cluster is running (not paused)
- Make sure you're using the correct connection string format with `+srv`

### OpenAI API Issues

- Verify your `OPENAI_API_KEY` is correct
- Check your OpenAI API credits and usage limits
- Ensure the API key has the necessary permissions

### CORS Issues

- The backend is configured to allow requests from `http://localhost:3000` and `http://localhost:3001`
- Update the CORS settings in `backend/main.py` if using different ports

## License

This project is provided as-is for educational and development purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
