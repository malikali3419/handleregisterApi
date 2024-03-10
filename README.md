
# Handleregister Project

A Django project for handling registrations, web scraping, and file downloads.

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

- Python 3.x
- Django
- Redis (for Celery task queue)

### Installing

1. **Clone the repository:**

   ```bash
   git clone https://github.com/malikali3419/handleregisterApi.git
   ```

2. **Change into the project directory:**

   ```bash
   cd handleregisterproject
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**

   ```bash
   python manage.py migrate
   ```

### Running the Development Server

```bash
python manage.py runserver
```

The development server will be available at [http://localhost:8000/](http://localhost:8000/).

### Running Celery Worker

```bash
celery -A core  worker --loglevel=info      
```

### Usage
- **Signup:**
   ```bash
   curl -X POST -d "username=your_username&password=your_password&email=your_email" http://localhost:8000/signup/
   ```
- **Login:**
   ```bash
   curl -X POST -d "email=your_email&password=your_password" http://localhost:8000/login/

   ```
- **Initiate Scraping and Downloading:**

  ```bash
  curl http://localhost:8000/process-results/{keyword}/
  ```

  Example:

  ```bash
  curl http://localhost:8000/process-results/example_keyword/
  ```

- **Get Results for a Company:**

  ```bash
  curl http://localhost:8000/get-results/{company}/
  ```

  Example:

  ```bash
  curl http://localhost:8000/get-results/example_company/
  ```

- **Download a File:**

  ```bash
  curl http://localhost:8000/download/{keyword}/{file_path}/ --output downloaded_file.pdf
  ```

  Example:

  ```bash
  curl http://localhost:8000/download/example_keyword/example_file.pdf --output downloaded_file.pdf
  ```

## Built With

- Django - The web framework used
- Celery - Distributed task queue
- Selenium - Web scraping tool
EOF
