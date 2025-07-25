# this_file: tests/test_font_info.py
"""Tests for font information extraction."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from font_organizer import (
    FontInfo,
    FontMetadata,
    FontStyle,
    FontWeight,
    FontNotFoundError,
    FontParseError,
)


class TestFontWeight:
    """Test FontWeight enum functionality."""

    def test_from_value(self):
        """Test creating FontWeight from numeric value."""
        assert FontWeight.from_value(100) == FontWeight.THIN
        assert FontWeight.from_value(400) == FontWeight.REGULAR
        assert FontWeight.from_value(700) == FontWeight.BOLD
        assert FontWeight.from_value(900) == FontWeight.BLACK
        
        # Test closest match
        assert FontWeight.from_value(450) == FontWeight.REGULAR
        assert FontWeight.from_value(550) == FontWeight.MEDIUM
        assert FontWeight.from_value(650) == FontWeight.SEMI_BOLD

    def test_from_string(self):
        """Test parsing FontWeight from string."""
        assert FontWeight.from_string("thin") == FontWeight.THIN
        assert FontWeight.from_string("regular") == FontWeight.REGULAR
        assert FontWeight.from_string("bold") == FontWeight.BOLD
        assert FontWeight.from_string("black") == FontWeight.BLACK
        
        # Test variations
        assert FontWeight.from_string("extra-light") == FontWeight.EXTRA_LIGHT
        assert FontWeight.from_string("semibold") == FontWeight.SEMI_BOLD
        assert FontWeight.from_string("normal") == FontWeight.REGULAR
        
        # Test default
        assert FontWeight.from_string("unknown") == FontWeight.REGULAR


class TestFontInfo:
    """Test FontInfo class."""

    @pytest.fixture
    def mock_ttfont(self):
        """Create a mock TTFont object."""
        mock_font = MagicMock()
        
        # Mock name table
        mock_name_record = Mock()
        mock_name_record.nameID = 1
        mock_name_record.platformID = 3
        mock_name_record.toUnicode.return_value = "Test Font"
        
        mock_name_table = Mock()
        mock_name_table.names = [mock_name_record]
        mock_font.__getitem__.side_effect = lambda key: {
            "name": mock_name_table,
            "OS/2": Mock(usWeightClass=400),
            "head": Mock(unitsPerEm=1000),
            "hhea": Mock(ascent=800, descent=-200, lineGap=100),
            "maxp": Mock(numGlyphs=256),
            "cmap": Mock(getBestCmap=lambda: {65: "A", 66: "B", 67: "C"}),
        }.get(key)
        
        mock_font.__contains__.side_effect = lambda key: key in [
            "name", "OS/2", "head", "hhea", "maxp", "cmap"
        ]
        
        return mock_font

    @patch("font_organizer.core.font_info.TTFont")
    @patch("font_organizer.core.font_info.Path.exists")
    @patch("font_organizer.core.font_info.Path.stat")
    def test_font_info_creation(self, mock_stat, mock_exists, mock_ttfont_class, mock_ttfont):
        """Test creating FontInfo instance."""
        mock_exists.return_value = True
        mock_stat.return_value = Mock(st_size=12345)
        mock_ttfont_class.return_value = mock_ttfont
        
        # Mock file operations
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = b"test"
            
            font_info = FontInfo("test.ttf")
            
            assert font_info.path == Path("test.ttf")
            assert font_info.family == "Test Font"
            assert font_info.metadata.file_size == 12345

    def test_font_not_found(self):
        """Test FontNotFoundError when file doesn't exist."""
        with patch("font_organizer.core.font_info.Path.exists", return_value=False):
            with pytest.raises(FontNotFoundError) as exc_info:
                FontInfo("nonexistent.ttf")
            assert "Font file not found: nonexistent.ttf" in str(exc_info.value)

    @patch("font_organizer.core.font_info.TTFont")
    @patch("font_organizer.core.font_info.Path.exists")
    def test_font_parse_error(self, mock_exists, mock_ttfont_class):
        """Test FontParseError when font cannot be parsed."""
        mock_exists.return_value = True
        mock_ttfont_class.side_effect = Exception("Invalid font")
        
        with pytest.raises(FontParseError) as exc_info:
            FontInfo("invalid.ttf")
        assert "Failed to parse font" in str(exc_info.value)
        assert "Invalid font" in str(exc_info.value)

    @patch("font_organizer.core.font_info.TTFont")
    @patch("font_organizer.core.font_info.Path.exists")
    @patch("font_organizer.core.font_info.Path.stat")
    def test_metadata_extraction(self, mock_stat, mock_exists, mock_ttfont_class, mock_ttfont):
        """Test metadata extraction from font."""
        mock_exists.return_value = True
        mock_stat.return_value = Mock(st_size=12345)
        mock_ttfont_class.return_value = mock_ttfont
        
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = b"test"
            
            font_info = FontInfo("test.ttf")
            metadata = font_info.metadata
            
            assert metadata.family == "Test Font"
            assert metadata.file_size == 12345
            assert metadata.format == "TTF"
            assert metadata.glyph_count == 256
            assert metadata.weight == FontWeight.REGULAR

    @patch("font_organizer.core.font_info.TTFont")
    @patch("font_organizer.core.font_info.Path.exists")
    @patch("font_organizer.core.font_info.Path.stat")
    def test_character_coverage(self, mock_stat, mock_exists, mock_ttfont_class, mock_ttfont):
        """Test character coverage functionality."""
        mock_exists.return_value = True
        mock_stat.return_value = Mock(st_size=12345)
        mock_ttfont_class.return_value = mock_ttfont
        
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = b"test"
            
            font_info = FontInfo("test.ttf")
            
            # Test has_character
            assert font_info.has_character("A")
            assert font_info.has_character(65)
            assert not font_info.has_character("Z")
            
            # Test characters property
            chars = font_info.characters
            assert 65 in chars
            assert 66 in chars
            assert 67 in chars


class TestFontMetadata:
    """Test FontMetadata dataclass."""

    def test_default_values(self):
        """Test FontMetadata default values."""
        metadata = FontMetadata()
        
        assert metadata.family == ""
        assert metadata.subfamily == ""
        assert metadata.style == FontStyle.REGULAR
        assert metadata.weight == FontWeight.REGULAR
        assert metadata.glyph_count == 0
        assert metadata.features == []
        assert metadata.unicode_ranges == []

    def test_custom_values(self):
        """Test FontMetadata with custom values."""
        metadata = FontMetadata(
            family="Custom Font",
            subfamily="Bold Italic",
            style=FontStyle.ITALIC,
            weight=FontWeight.BOLD,
            glyph_count=500,
        )
        
        assert metadata.family == "Custom Font"
        assert metadata.subfamily == "Bold Italic"
        assert metadata.style == FontStyle.ITALIC
        assert metadata.weight == FontWeight.BOLD
        assert metadata.glyph_count == 500