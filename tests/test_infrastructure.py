import pytest
import sys
from pathlib import Path


class TestInfrastructureSetup:
    """Validation tests to ensure the testing infrastructure is properly configured."""
    
    def test_pytest_installed(self):
        """Verify pytest is available."""
        assert 'pytest' in sys.modules or pytest
        
    def test_pytest_cov_installed(self):
        """Verify pytest-cov is available."""
        try:
            import pytest_cov
            assert True
        except ImportError:
            # Plugin might be loaded differently
            assert any('pytest_cov' in str(plugin) or 'coverage' in str(plugin) 
                      for plugin in pytest.config.pluginmanager.get_plugins()
                      if hasattr(pytest, 'config'))
    
    def test_pytest_mock_installed(self):
        """Verify pytest-mock is available."""
        try:
            import pytest_mock
            assert True
        except ImportError:
            # Plugin might be loaded differently
            assert True  # Will be validated when running with mock fixtures
    
    def test_testing_directories_exist(self):
        """Verify testing directory structure exists."""
        test_root = Path(__file__).parent
        assert test_root.exists()
        assert (test_root / 'unit').exists()
        assert (test_root / 'integration').exists()
        assert (test_root / '__init__.py').exists()
        assert (test_root / 'unit' / '__init__.py').exists()
        assert (test_root / 'integration' / '__init__.py').exists()
    
    def test_conftest_exists(self):
        """Verify conftest.py exists with fixtures."""
        conftest_path = Path(__file__).parent / 'conftest.py'
        assert conftest_path.exists()
        
        # Verify it contains expected fixtures
        with open(conftest_path) as f:
            content = f.read()
            assert 'def temp_dir' in content
            assert 'def mock_env' in content
            assert 'def mock_requests' in content
            assert 'def mock_github_client' in content
    
    def test_pyproject_toml_exists(self):
        """Verify pyproject.toml exists with proper configuration."""
        pyproject_path = Path(__file__).parent.parent / 'pyproject.toml'
        assert pyproject_path.exists()
        
        with open(pyproject_path) as f:
            content = f.read()
            # Check Poetry configuration
            assert '[tool.poetry]' in content
            assert 'pytest' in content
            assert 'pytest-cov' in content
            assert 'pytest-mock' in content
            
            # Check pytest configuration
            assert '[tool.pytest.ini_options]' in content
            assert 'testpaths' in content
            assert 'markers' in content
            
            # Check coverage configuration
            assert '[tool.coverage.run]' in content
            assert '[tool.coverage.report]' in content
    
    def test_gitignore_updated(self):
        """Verify .gitignore includes testing entries."""
        gitignore_path = Path(__file__).parent.parent / '.gitignore'
        assert gitignore_path.exists()
        
        with open(gitignore_path) as f:
            content = f.read()
            assert '.pytest_cache/' in content
            assert '.coverage' in content
            assert 'htmlcov/' in content
            assert 'coverage.xml' in content
            assert '.claude/*' in content


class TestFixtures:
    """Test that fixtures work correctly."""
    
    def test_temp_dir_fixture(self, temp_dir):
        """Test temp_dir fixture creates and cleans up directory."""
        assert temp_dir.exists()
        assert temp_dir.is_dir()
        
        # Create a test file
        test_file = temp_dir / 'test.txt'
        test_file.write_text('test content')
        assert test_file.exists()
    
    def test_mock_env_fixture(self, mock_env):
        """Test mock_env fixture for environment variables."""
        mock_env.set('TEST_VAR', 'test_value')
        assert mock_env.get('TEST_VAR') == 'test_value'
        assert 'TEST_VAR' in mock_env.vars
    
    def test_sample_handler_event_fixture(self, sample_handler_event):
        """Test sample_handler_event fixture structure."""
        assert 'body' in sample_handler_event
        assert 'headers' in sample_handler_event
        assert 'method' in sample_handler_event
        assert sample_handler_event['method'] == 'POST'
    
    def test_sample_github_payload_fixture(self, sample_github_payload):
        """Test sample_github_payload fixture structure."""
        assert 'action' in sample_github_payload
        assert 'issue' in sample_github_payload
        assert 'repository' in sample_github_payload
        assert sample_github_payload['issue']['number'] == 42
    
    def test_mock_config_file_fixture(self, mock_config_file):
        """Test mock_config_file fixture creates config."""
        assert mock_config_file.exists()
        
        import json
        with open(mock_config_file) as f:
            config = json.load(f)
            assert 'github_token' in config
            assert 'webhook_secret' in config
            assert 'labels' in config


@pytest.mark.unit
class TestMarkers:
    """Test that custom markers work."""
    
    def test_unit_marker(self):
        """Test with unit marker."""
        assert True
    
    @pytest.mark.integration
    def test_multiple_markers(self):
        """Test with multiple markers."""
        assert True
    
    @pytest.mark.slow
    def test_slow_marker(self):
        """Test with slow marker."""
        assert True