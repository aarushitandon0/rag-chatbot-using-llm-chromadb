# agents/github_search_agent.py
import sys
sys.path.append("C:/Users/AARUSHI TANDON/OneDrive/Python/DevSync")

import requests
import json
import re
from google_adk.framework.agent import Agent
from google_adk.framework.message import Message

class GitHubSearchAgent(Agent):
    def __init__(self):
        super().__init__()
        self.name = "GitHubSearchAgent"

    def extract_keywords(self, text):
        keyword_list = [
            "chatbot", "virtual assistant", "recommendation", "news", "weather", "calendar", "reminder", "todo",
            "note", "journal", "habit", "tracker", "fitness", "workout", "diet", "nutrition", "recipe", "meal",
            "planner", "grocery", "shopping", "budget", "expense", "finance", "investment", "stock", "crypto",
            "wallet", "blockchain", "nft", "defi", "payment", "invoice", "billing", "tax", "banking", "loan",
            "credit", "score", "insurance", "health", "telemedicine", "appointment", "doctor", "pharmacy",
            "mental", "wellness", "therapy", "meditation", "sleep", "alarm", "study", "learning", "quiz",
            "flashcard", "exam", "test", "language", "translation", "dictionary", "grammar", "spelling",
            "reading", "book", "library", "ebook", "audiobook", "podcast", "music", "player", "streaming",
            "video", "movie", "tv", "series", "media", "editor", "photo", "image", "gallery", "camera",
            "filter", "animation", "drawing", "painting", "design", "logo", "poster", "flyer", "resume",
            "portfolio", "website", "landing", "blog", "cms", "ecommerce", "shop", "cart", "order", "delivery",
            "restaurant", "menu", "reservation", "event", "ticket", "booking", "travel", "trip", "flight",
            "hotel", "map", "navigation", "gps", "ride", "taxi", "carpool", "parking", "public", "transport",
            "bus", "train", "metro", "bike", "scooter", "game", "puzzle", "quiz", "trivia", "arcade", "platformer",
            "multiplayer", "leaderboard", "score", "achievement", "badge", "social", "network", "community",
            "forum", "chat", "messenger", "group", "video call", "voice", "conference", "collaboration",
            "team", "project", "kanban", "scrum", "agile", "task", "management", "crm", "erp", "inventory",
            "supply", "chain", "logistics", "warehouse", "shipping", "tracking", "order", "customer", "support",
            "helpdesk", "faq", "ticket", "survey", "poll", "feedback", "review", "rating", "comment", "vote",
            "petition", "campaign", "donation", "fundraising", "charity", "volunteer", "ngo", "environment",
            "sustainability", "recycling", "waste", "energy", "solar", "wind", "water", "conservation",
            "climate", "carbon", "footprint", "green", "plant", "tree", "garden", "agriculture", "farm",
            "crop", "livestock", "food", "security", "nutrition", "hunger", "poverty", "education", "school",
            "student", "teacher", "classroom", "course", "lesson", "tutor", "mentor", "scholarship", "grant",
            "job", "career", "resume", "cv", "interview", "internship", "freelance", "gig", "marketplace",
            "portfolio", "networking", "recruitment", "hr", "payroll", "attendance", "leave", "timesheet",
            "productivity", "focus", "timer", "pomodoro", "distraction", "blocker", "goal", "milestone",
            "roadmap", "timeline", "calendar", "schedule", "sync", "integration", "api", "webhook", "automation",
            "bot", "scraper", "crawler", "parser", "extractor", "data", "mining", "analysis", "analytics",
            "dashboard", "report", "visualization", "chart", "graph", "plot", "map", "heatmap", "infographic",
            "statistics", "prediction", "forecast", "machine learning", "ml", "ai", "deep learning", "neural",
            "network", "classification", "regression", "clustering", "nlp", "speech", "voice", "recognition",
            "sentiment", "emotion", "translation", "summarization", "question answering", "search", "ranking",
            "recommendation", "personalization", "security", "privacy", "encryption", "decryption", "password",
            "vault", "locker", "authentication", "authorization", "oauth", "jwt", "captcha", "2fa", "biometric",
            "face", "fingerprint", "iris", "voice", "detection", "spam", "phishing", "malware", "firewall",
            "vpn", "proxy", "monitor", "alert", "notification", "log", "audit", "compliance", "gdpr", "hipaa",
            "backup", "restore", "sync", "cloud", "storage", "drive", "file", "document", "pdf", "docx",
            "excel", "spreadsheet", "presentation", "slide", "markdown", "html", "css", "js", "typescript",
            "python", "java", "csharp", "cpp", "go", "rust", "php", "ruby", "swift", "kotlin", "scala",
            "perl", "shell", "bash", "powershell", "docker", "kubernetes", "devops", "ci", "cd", "pipeline",
            "test", "unit", "integration", "e2e", "mock", "stub", "benchmark", "performance", "optimizer",
            "seo", "ads", "marketing", "campaign", "crm", "lead", "prospect", "conversion", "sales", "invoice",
            "billing", "payment", "stripe", "paypal", "bitcoin", "ethereum", "exchange", "wallet", "defi",
            "nft", "auction", "bidding", "marketplace", "shop", "store", "cart", "checkout", "order", "delivery",
            "shipping", "tracking", "return", "refund", "support", "helpdesk", "faq", "wiki", "documentation",
            "guide", "tutorial", "course", "lesson", "blog", "news", "newsletter", "rss", "feed", "alert",
            "push", "sms", "email", "smtp", "imap", "pop3", "calendar", "event", "invite", "reminder", "meeting",
            "conference", "webinar", "livestream", "broadcast", "media", "player", "recorder", "editor",
            "converter", "compressor", "optimizer", "gallery", "album", "slideshow", "animation", "3d", "2d",
            "render", "graphics", "opengl", "vulkan", "unity", "unreal", "game", "engine", "physics", "ai",
            "pathfinding", "multiplayer", "leaderboard", "achievement", "badge", "profile", "avatar", "skin",
            "theme", "customization", "settings", "config", "setup", "install", "update", "upgrade", "patch",
            "release", "changelog", "version", "git", "github", "gitlab", "bitbucket", "svn", "mercurial",
            "jira", "trello", "asana", "notion", "slack", "discord", "telegram", "whatsapp", "messenger",
            "sms", "push", "notification", "alert", "log", "monitor", "metrics", "prometheus", "grafana",
            "elk", "splunk", "sentry", "bug", "issue", "ticket", "support", "helpdesk", "faq", "wiki"
        ]
        pattern = r'\b(' + '|'.join(re.escape(k) for k in keyword_list) + r')\b'
        keywords = re.findall(pattern, text.lower())

        # fallback: top 5 unique words
        if not keywords:
            keywords = list(dict.fromkeys(text.lower().split()))[:5]

        return "+".join(keywords)

    def run(self, message: Message) -> Message:
        query = self.extract_keywords(message.content)
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=5"

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "User"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            results = []
            for repo in data.get("items", []):
                if not repo.get("description"):
                    continue
                results.append({
                    "name": repo.get("full_name"),
                    "description": repo.get("description"),
                    "stars": repo.get("stargazers_count"),
                    "url": repo.get("html_url")
                })

            if not results:
                return Message(content="[]")

            return Message(content=json.dumps(results, indent=2))

        except Exception as e:
            return Message(content=json.dumps({"error": str(e)}))
