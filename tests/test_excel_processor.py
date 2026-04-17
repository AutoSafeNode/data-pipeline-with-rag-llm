"""
Test cases for Excel Processor
"""

import pytest
import asyncio
from pathlib import Path
from src_python.processors.excel_processor import ExcelProcessor
from src_python.utils.config import PipelineConfig


class TestExcelProcessor:
    """Test cases for Excel processor."""
    
    @pytest.fixture
    def sample_config(self):
        """Create sample configuration for testing."""
        return PipelineConfig(
            input_dir="./tests/data/excel",
            output_dir="./tests/output",
            chunk_size=1000,
            chunk_overlap=200
        )
    
    @pytest.fixture
    def processor(self, sample_config):
        """Create Excel processor instance."""
        return ExcelProcessor(sample_config)
    
    @pytest.mark.asyncio
    async def test_read_excel_not_found(self, processor):
        """Test reading non-existent Excel file."""
        with pytest.raises(FileNotFoundError):
            await processor.read_excel("nonexistent.xlsx")
    
    @pytest.mark.asyncio
    async def test_convert_to_chunks_empty_data(self, processor):
        """Test converting empty Excel data to chunks."""
        result = await processor.convert_to_chunks([])
        assert result == []
    
    def test_clean_data(self, processor):
        """Test data cleaning functionality."""
        test_data = [
            ("A", "B", "C"),
            (None, None, None),
            ("D", "E", "F")
        ]
        cleaned = processor._clean_data(test_data)
        assert len(cleaned) == 2
        assert cleaned[0] == ("A", "B", "C")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
