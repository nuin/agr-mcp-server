# utils.py
"""Utility functions and enhanced configuration management for AGR MCP Server."""

import os
import yaml
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AGRConfig:
    """Configuration class for AGR MCP Server."""
    base_url: str = "https://www.alliancegenome.org/api"
    blast_url: str = "https://blast.alliancegenome.org"
    fms_url: str = "https://fms.alliancegenome.org/api"
    timeout: float = 30.0
    rate_limit: int = 100
    rate_limit_window: int = 60
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> 'AGRConfig':
        """Load configuration from environment variables."""
        return cls(
            base_url=os.getenv("AGR_BASE_URL", cls.base_url),
            blast_url=os.getenv("AGR_BLAST_URL", cls.blast_url),
            fms_url=os.getenv("AGR_FMS_URL", cls.fms_url),
            timeout=float(os.getenv("AGR_TIMEOUT", cls.timeout)),
            rate_limit=int(os.getenv("AGR_RATE_LIMIT", cls.rate_limit)),
            rate_limit_window=int(os.getenv("AGR_RATE_LIMIT_WINDOW", cls.rate_limit_window)),
            log_level=os.getenv("LOG_LEVEL", cls.log_level)
        )

    @classmethod
    def from_yaml(cls, config_path: str = "config.yaml") -> 'AGRConfig':
        """Load configuration from YAML file."""
        config_file = Path(config_path)
        if not config_file.exists():
            return cls.from_env()
        
        with open(config_file, 'r') as f:
            config_data = yaml.safe_load(f)
        
        agr_config = config_data.get("agr", {})
        return cls(
            base_url=agr_config.get("base_url", cls.base_url),
            blast_url=agr_config.get("blast_url", cls.blast_url),
            fms_url=agr_config.get("fms_url", cls.fms_url),
            timeout=agr_config.get("timeout", cls.timeout),
            rate_limit=agr_config.get("rate_limit", cls.rate_limit),
            rate_limit_window=agr_config.get("rate_limit_window", cls.rate_limit_window),
            log_level=config_data.get("logging", {}).get("level", cls.log_level)
        )

def setup_logging(config: AGRConfig):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, config.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("agr_mcp_server.log")
        ]
    )

def validate_gene_id(gene_id: str) -> bool:
    """Validate gene identifier format."""
    valid_prefixes = [
        "HGNC:", "MGI:", "ZFIN:", "FB:", "WB:", "SGD:", "RGD:",
        "ENSEMBL:", "RefSeq:", "UniProt:"
    ]
    return any(gene_id.startswith(prefix) for prefix in valid_prefixes)

def validate_sequence(sequence: str) -> bool:
    """Validate DNA/RNA/protein sequence."""
    # Remove whitespace and convert to uppercase
    clean_seq = sequence.replace(" ", "").replace("\n", "").upper()
    
    # Check for valid nucleotide sequence
    nucleotides = set("ATCGUN")
    if all(c in nucleotides for c in clean_seq):
        return True
    
    # Check for valid amino acid sequence
    amino_acids = set("ACDEFGHIKLMNPQRSTVWY")
    if all(c in amino_acids for c in clean_seq):
        return True
    
    return False

def format_gene_result(gene_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format gene search result for better readability."""
    return {
        "id": gene_data.get("id", ""),
        "symbol": gene_data.get("symbol", ""),
        "name": gene_data.get("name", ""),
        "species": gene_data.get("species", {}).get("name", ""),
        "description": gene_data.get("automatedGeneSynopsis", ""),
        "synonyms": gene_data.get("synonyms", []),
        "gene_type": gene_data.get("soTermName", ""),
        "chromosome": gene_data.get("genomeLocations", [{}])[0].get("chromosome", "") if gene_data.get("genomeLocations") else "",
    }

def format_disease_result(disease_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format disease association result."""
    return {
        "disease_id": disease_data.get("diseaseId", ""),
        "disease_name": disease_data.get("diseaseName", ""),
        "association_type": disease_data.get("associationType", ""),
        "evidence_codes": disease_data.get("evidenceCodes", []),
        "publications": [pub.get("pubMedId") for pub in disease_data.get("publications", [])],
        "source": disease_data.get("source", {}).get("name", "")
    }
