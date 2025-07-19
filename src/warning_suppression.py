#!/usr/bin/env python3
"""
Warning suppression utilities for AI Dev Agents
"""

import warnings
import logging
from typing import Optional

def suppress_warnings():
    """Suppress common warnings that don't affect functionality"""
    
    # Suppress urllib3 SSL warnings
    warnings.filterwarnings(
        "ignore",
        message="urllib3 v2 only supports OpenSSL 1.1.1+",
        category=UserWarning,
        module="urllib3"
    )
    
    # Suppress Pydantic V1/V2 mixing warnings
    warnings.filterwarnings(
        "ignore",
        message="Mixing V1 models and V2 models",
        category=UserWarning,
        module="pydantic"
    )
    
    # Suppress other common warnings
    warnings.filterwarnings(
        "ignore",
        message=".*deprecated.*",
        category=DeprecationWarning
    )

def configure_logging(level: int = logging.INFO, suppress_warnings_flag: bool = True):
    """Configure logging with optional warning suppression"""
    
    if suppress_warnings_flag:
        suppress_warnings()
    
    # Configure logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
        ]
    )
    
    # Set specific logger levels to reduce noise
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("pydantic").setLevel(logging.WARNING)
    logging.getLogger("crewai").setLevel(logging.INFO)

def get_clean_environment():
    """Get a clean environment with warnings suppressed"""
    suppress_warnings()
    return True 