import os
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.schemas.email_schema import EmailRequest
from app.providers.base_provider import EmailProvider

# Initialize Jinja2 environment for templates
template_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'templates')
)
jinja_env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=select_autoescape(['html', 'xml'])
)

class EmailService:
    def __init__(self, provider: EmailProvider):
        self.provider = provider

    def send(self, req: EmailRequest) -> None:
        """
        Render a Jinja2 html template if provided, otherwise use the raw body,
        then delegate to the configured EmailProvider.
        """
        # Determine final body and subtype
        if req.template_name:
            try:
                template = jinja_env.get_template(req.template_name)
                rendered_body = template.render(**(req.template_data or {}))
                req.body = rendered_body
            except Exception as e:
                raise RuntimeError(f"Template rendering error: {e}")

        # Delegate sending to provider
        self.provider.send_email(req)