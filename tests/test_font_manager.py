# this_file: tests/test_font_manager.py
"""Tests for FontManager class."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from font_organizer import (
    FontManager,
    Config,
    FontInfo,
    FontMetadata,
)


class TestFontManager:
    """Test FontManager class."""

    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return Config()

    @pytest.fixture
    def manager(self, config):
        """Create FontManager instance."""
        return FontManager(config)

    def test_manager_creation(self, config):
        """Test creating FontManager instance."""
        manager = FontManager(config)
        assert manager.config == config
        assert isinstance(manager._font_cache, dict)

    @patch("font_organizer.core.font_manager.load_config")
    def test_manager_default_config(self, mock_load_config):
        """Test FontManager with default config."""
        mock_config = Config()
        mock_load_config.return_value = mock_config
        
        manager = FontManager()
        assert manager.config == mock_config
        mock_load_config.assert_called_once()

    @patch("font_organizer.core.font_manager.FontInfo")
    def test_get_font_info_caching(self, mock_font_info_class, manager):
        """Test font info caching."""
        mock_font_info = Mock()
        mock_font_info_class.return_value = mock_font_info
        
        # First call should create new FontInfo
        info1 = manager.get_font_info("test.ttf")
        assert info1 == mock_font_info
        mock_font_info_class.assert_called_once()
        
        # Second call should return cached instance
        info2 = manager.get_font_info("test.ttf")
        assert info2 == mock_font_info
        assert mock_font_info_class.call_count == 1

    @patch("font_organizer.core.font_manager.Path.glob")
    @patch("font_organizer.core.font_manager.Path.exists")
    @patch("font_organizer.core.font_manager.Path.is_dir")
    def test_scan_directory(self, mock_is_dir, mock_exists, mock_glob, manager):
        """Test directory scanning."""
        mock_exists.return_value = True
        mock_is_dir.return_value = True
        
        # Mock font files
        mock_files = [
            Mock(is_file=lambda: True, match=lambda p: False),
            Mock(is_file=lambda: True, match=lambda p: False),
        ]
        for i, f in enumerate(mock_files):
            f.__str__ = lambda i=i: f"font{i}.ttf"
            f.__lt__ = lambda self, other: str(self) < str(other)
            f.__gt__ = lambda self, other: str(self) > str(other)
            f.__eq__ = lambda self, other: str(self) == str(other)
            f.__hash__ = lambda self: hash(str(self))
        
        mock_glob.return_value = mock_files
        
        fonts = manager.scan_directory("/test/dir")
        
        assert len(fonts) == 2
        mock_exists.assert_called_once()
        mock_is_dir.assert_called_once()

    def test_scan_nonexistent_directory(self, manager):
        """Test scanning nonexistent directory."""
        with patch("font_organizer.core.font_manager.Path.exists", return_value=False):
            fonts = manager.scan_directory("/nonexistent")
            assert fonts == []

    @patch("font_organizer.core.font_manager.FontInfo")
    def test_analyze_fonts(self, mock_font_info_class, manager):
        """Test font analysis."""
        # Create mock font info
        mock_metadata = FontMetadata(
            family="Test Font",
            format="TTF",
            file_size=1000,
            vendor="Test Vendor",
        )
        mock_info = Mock()
        mock_info.family = "Test Font"
        mock_info.metadata = mock_metadata
        mock_info.weight.name = "REGULAR"
        mock_info.style.name = "REGULAR"
        mock_info.features = ["kern", "liga"]
        
        mock_font_info_class.return_value = mock_info
        
        # Analyze fonts
        font_paths = [Path("font1.ttf"), Path("font2.ttf")]
        analysis = manager.analyze_fonts(font_paths)
        
        assert analysis["total_fonts"] == 2
        assert analysis["total_size"] == 2000
        assert analysis["formats"]["TTF"] == 2
        assert "Test Font" in analysis["families"]
        assert len(analysis["families"]["Test Font"]) == 2

    @patch("font_organizer.core.font_manager.FontInfo")
    def test_find_duplicates(self, mock_font_info_class, manager):
        """Test duplicate detection."""
        # Create mock font infos with different hashes
        mock_info1 = Mock()
        mock_info1.metadata.file_hash = "hash1"
        
        mock_info2 = Mock()
        mock_info2.metadata.file_hash = "hash1"  # Same hash
        
        mock_info3 = Mock()
        mock_info3.metadata.file_hash = "hash2"  # Different hash
        
        mock_font_info_class.side_effect = [mock_info1, mock_info2, mock_info3]
        
        font_paths = [Path("font1.ttf"), Path("font2.ttf"), Path("font3.ttf")]
        duplicates = manager.find_duplicates(font_paths)
        
        assert len(duplicates) == 1
        assert len(duplicates[0]) == 2

    def test_get_system_font_dirs_linux(self, manager):
        """Test getting system font directories on Linux."""
        with patch("platform.system", return_value="Linux"):
            dirs = manager.get_system_font_dirs()
            
            # Should include standard Linux font directories
            dir_paths = [str(d) for d in dirs]
            assert any("/usr/share/fonts" in p for p in dir_paths)

    def test_get_system_font_dirs_macos(self, manager):
        """Test getting system font directories on macOS."""
        with patch("platform.system", return_value="Darwin"):
            dirs = manager.get_system_font_dirs()
            
            # Should include standard macOS font directories
            dir_paths = [str(d) for d in dirs]
            assert any("/Library/Fonts" in p for p in dir_paths)

    def test_get_system_font_dirs_windows(self, manager):
        """Test getting system font directories on Windows."""
        with patch("platform.system", return_value="Windows"):
            with patch.dict("os.environ", {"WINDIR": "C:\\Windows"}):
                dirs = manager.get_system_font_dirs()
                
                # Should include Windows font directory
                dir_paths = [str(d) for d in dirs]
                assert any("Fonts" in p for p in dir_paths)