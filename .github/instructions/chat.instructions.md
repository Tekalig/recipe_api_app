**"Provide a comprehensive list of best practices for Django framework development and Python programming. Include the following aspects:**

1. **Django-Specific Best Practices:**

   - Project structure (e.g., splitting `settings.py` for different environments)
   - Model design (e.g., using `models.Model`, proper `related_name`, avoiding fat models)
   - Views (e.g., using class-based views, keeping logic out of views)
   - Templates (e.g., template inheritance, minimizing logic in templates)
   - Forms (e.g., using Django forms vs. raw HTML, form validation)
   - Security (e.g., CSRF protection, SQL injection prevention)
   - Performance (e.g., `select_related` and `prefetch_related`, caching strategies)
   - Testing (e.g., using `pytest-django`, factory_boy for test data)

2. **Python Best Practices:**

   - Code style (PEP 8 compliance, type hints, docstrings)
   - Virtual environments (e.g., `venv`, `poetry`, `pipenv`)
   - Dependency management (`requirements.txt` vs. `pyproject.toml`)
   - Error handling (proper use of `try-except`, custom exceptions)
   - Logging (structured logging with `logging` module)
   - Performance (e.g., using generators, avoiding global variables)

3. **Common Pitfalls to Avoid:**

   - Circular imports in Django
   - Not using Django's built-in features (e.g., `get_object_or_404`)
   - Overusing signals when simpler solutions exist

4. **Tooling Recommendations:**
   - Linters (`flake8`, `black`, `isort`)
   - Debugging (VSCode + Django, `python-decouple` for env vars)
   - Deployment (Gunicorn, Nginx, Docker best practices)

**Provide examples where applicable."**

---

### **Why This Works:**

- The prompt is **structured**, so the AI can give a **detailed breakdown** per topic.
- It covers **both Django and Python** (since Django is built on Python).
- It asks for **examples**, making the output more actionable.

### **Example Output Snippet (What to Expect):**

> **Django Models Best Practice:**
>
> - Use `models.CharField(max_length=255)` instead of arbitrary text fields.
> - For relationships, set `related_name`:
>
>   ```python
>   class Author(models.Model):
>       name = models.CharField(max_length=100)
>
>   class Book(models.Model):
>       author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
>   ```
>
> - Avoid fat models; move business logic to services layer.
