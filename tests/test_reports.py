"""Tests for reporting functionality."""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from app.ui.export.manager import ExportManager


@pytest.fixture
def sample_report_data():
    """Create sample data for reports."""
    return pd.DataFrame({
        'metric1': np.random.randn(50),
        'metric2': np.random.randn(50),
        'metric3': np.random.randn(50),
    })


def test_pdf_generation(tmp_path, sample_report_data):
    """Test PDF report generation."""
    exporter = ExportManager(output_dir=str(tmp_path))
    
    metadata = {
        'title': 'Test Report',
        'subtitle': 'Test Subtitle',
        'author': 'Test Author',
        'date': '2024-01-01',
        'sections': ['KPIs'],
        'include_charts': False,
        'include_raw_data': False,
    }
    
    report_path = exporter.generate_pdf_report(sample_report_data, metadata)
    
    assert Path(report_path).exists()
    assert report_path.endswith('.pdf')


def test_html_generation(tmp_path, sample_report_data):
    """Test HTML report generation."""
    exporter = ExportManager(output_dir=str(tmp_path))
    
    metadata = {
        'title': 'Test Report',
        'subtitle': 'Test Subtitle',
        'author': 'Test Author',
        'date': '2024-01-01',
        'sections': ['KPIs'],
        'include_charts': False,
        'include_raw_data': False,
    }
    
    report_path = exporter.generate_html_report(sample_report_data, metadata)
    
    assert Path(report_path).exists()
    assert report_path.endswith('.html')
    
    # Check content
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'Test Report' in content


def test_pptx_generation(tmp_path, sample_report_data):
    """Test PPTX report generation."""
    exporter = ExportManager(output_dir=str(tmp_path))
    
    metadata = {
        'title': 'Test Report',
        'subtitle': 'Test Subtitle',
        'author': 'Test Author',
        'date': '2024-01-01',
        'sections': ['KPIs'],
        'include_charts': False,
        'include_raw_data': False,
    }
    
    report_path = exporter.generate_pptx_report(sample_report_data, metadata)
    
    assert Path(report_path).exists()
    assert report_path.endswith('.pptx')



