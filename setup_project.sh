#!/bin/bash

# Set project name
PROJECT_NAME="Career_Recommendation_System"


# Create backend structure
mkdir -p backend/app/{routes,services,models,utils}
touch backend/app/{routes/__init__.py,routes/recommendations.py,routes/users.py,routes/health.py}
touch backend/app/{services/__init__.py,services/llama_service.py,services/chromadb_service.py,services/user_service.py}
touch backend/app/{models/__init__.py,models/recommendation.py,models/user.py}
touch backend/app/{utils/__init__.py,utils/embedding.py,utils/logger.py}
touch backend/app/config.py backend/app/main.py
touch backend/requirements.txt backend/.env

# Create frontend structure
mkdir -p frontend/{public,src/{components,pages,services,context}}
touch frontend/src/components/{QuestionCard.js,RecommendationList.js}
touch frontend/src/pages/{Home.js,Results.js}
touch frontend/src/services/api.js
touch frontend/src/context/CareerContext.js
touch frontend/src/{App.js,index.js}
touch frontend/package.json frontend/.env

# Create documentation folder
mkdir -p docs
touch docs/{README.md,API_DOCS.md}

# Create scripts folder
mkdir -p scripts
touch scripts/{deploy.sh,setup.sh}

# Create tests folder
mkdir -p tests/{backend,frontend}

# Create project root files
touch .gitignore docker-compose.yml Dockerfile

# Output success message
echo "✅ Folder structure for $PROJECT_NAME created successfully!"
