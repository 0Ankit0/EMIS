"""
Translation helper for internationalization (i18n)
"""

import json
import os
from functools import lru_cache
from typing import Dict, Optional


class Translator:
    """Translation helper class"""

    def __init__(self, default_language: str = "en"):
        """Initialize translator with default language"""
        self.default_language = default_language
        self.translations: Dict[str, Dict] = {}
        self._load_translations()

    def _load_translations(self):
        """Load translation files from i18n directory"""
        i18n_dir = os.path.dirname(os.path.abspath(__file__))

        # Load available language files
        for filename in os.listdir(i18n_dir):
            if filename.endswith(".json"):
                language_code = filename.replace(".json", "")
                filepath = os.path.join(i18n_dir, filename)

                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        self.translations[language_code] = json.load(f)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error loading translation file {filename}: {e}")

    @lru_cache(maxsize=1000)
    def get(self, key: str, language: Optional[str] = None, **kwargs) -> str:
        """
        Get translated string by key

        Args:
            key: Translation key (dot notation, e.g., 'auth.login_success')
            language: Target language code (defaults to default_language)
            **kwargs: Variables to substitute in the translation string

        Returns:
            Translated string with substituted variables

        Examples:
            >>> translator.get('auth.login_success')
            'Login successful'
            >>> translator.get('validation.min_length', min=8)
            'Minimum length is 8'
        """
        if language is None:
            language = self.default_language

        # Get translation dict for language, fallback to default
        trans_dict = self.translations.get(
            language, self.translations.get(self.default_language, {})
        )

        # Navigate nested dictionary using dot notation
        keys = key.split(".")
        value = trans_dict

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                value = None
                break

        # If translation not found, return the key itself
        if value is None or not isinstance(value, str):
            return key

        # Substitute variables
        if kwargs:
            try:
                return value.format(**kwargs)
            except (KeyError, AttributeError):
                return value

        return value

    def translate(self, key: str, language: Optional[str] = None, **kwargs) -> str:
        """Alias for get() method"""
        return self.get(key, language, **kwargs)

    def add_language(self, language_code: str, translations: Dict):
        """
        Add or update translations for a language

        Args:
            language_code: Language code (e.g., 'es', 'fr', 'de')
            translations: Dictionary of translations
        """
        self.translations[language_code] = translations
        # Clear cache when translations change
        self.get.cache_clear()

    def get_available_languages(self) -> list:
        """Get list of available language codes"""
        return list(self.translations.keys())


# Global translator instance
_translator = Translator()


def translate(key: str, language: Optional[str] = None, **kwargs) -> str:
    """
    Global translation function

    Args:
        key: Translation key (dot notation)
        language: Target language code
        **kwargs: Variables to substitute

    Returns:
        Translated string

    Examples:
        >>> from apps.core.i18n import translate
        >>> translate('auth.login_success')
        'Login successful'
    """
    return _translator.translate(key, language, **kwargs)


def set_default_language(language: str):
    """Set the default language for translations"""
    _translator.default_language = language


def add_language(language_code: str, translations: Dict):
    """Add or update translations for a language"""
    _translator.add_language(language_code, translations)


def get_available_languages() -> list:
    """Get list of available language codes"""
    return _translator.get_available_languages()
