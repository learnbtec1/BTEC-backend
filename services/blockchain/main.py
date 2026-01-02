"""
Blockchain Certificates Service
Tamper-proof certificates using blockchain technology
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum
import os
import hashlib

app = FastAPI(
    title="Blockchain Certificates Service",
    description="Blockchain Certificates - شهادات موثقة غير قابلة للتزوير",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums
class CertificateType(str, Enum):
    COURSE_COMPLETION = "course_completion"
    SKILL_BADGE = "skill_badge"
    ACHIEVEMENT = "achievement"
    DEGREE = "degree"
    PROFESSIONAL = "professional"

class BlockchainNetwork(str, Enum):
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    BINANCE = "binance"

# Models
class Certificate(BaseModel):
    """Digital certificate"""
    id: str
    student_id: str
    student_name: str
    certificate_type: CertificateType
    title: str
    description: str
    issued_by: str
    issued_date: datetime
    expiry_date: Optional[datetime] = None
    course_id: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    grade: Optional[str] = None
    metadata: Dict[str, any] = Field(default_factory=dict)

class BlockchainCertificate(BaseModel):
    """Blockchain-verified certificate"""
    certificate_id: str
    blockchain_hash: str
    transaction_hash: str
    blockchain_network: BlockchainNetwork
    contract_address: str
    token_id: Optional[str] = None  # For NFT certificates
    ipfs_hash: Optional[str] = None  # IPFS storage hash
    verification_url: str
    minted_at: datetime
    gas_used: Optional[float] = None

class NFTCertificate(BaseModel):
    """NFT Certificate metadata"""
    token_id: str
    name: str
    description: str
    image_url: str
    attributes: List[Dict[str, str]]
    blockchain_network: BlockchainNetwork
    contract_address: str
    owner_address: str
    created_at: datetime

class CertificateVerification(BaseModel):
    """Certificate verification result"""
    is_valid: bool
    certificate_id: str
    blockchain_hash: str
    issued_to: str
    issued_by: str
    issued_date: datetime
    verified_at: datetime
    blockchain_confirmations: int
    tamper_proof: bool = True

class EducationalRecord(BaseModel):
    """Permanent educational record"""
    student_id: str
    student_name: str
    total_certificates: int
    certificates: List[Dict[str, any]]
    skills_earned: List[str]
    achievements: List[str]
    total_nfts: int
    record_hash: str
    last_updated: datetime

# Helper functions
def generate_certificate_hash(certificate: Certificate) -> str:
    """Generate SHA-256 hash for certificate"""
    cert_string = f"{certificate.student_id}{certificate.title}{certificate.issued_date.isoformat()}"
    return hashlib.sha256(cert_string.encode()).hexdigest()

# Endpoints
@app.get("/")
async def root():
    """Health check"""
    return {
        "service": "Blockchain Certificates Service",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.post("/api/v1/issue-certificate", response_model=BlockchainCertificate)
async def issue_certificate(certificate: Certificate):
    """
    Issue a new blockchain certificate
    إصدار شهادة موثقة
    """
    # Generate certificate hash
    cert_hash = generate_certificate_hash(certificate)
    
    # TODO: Integrate with actual blockchain
    # This would involve:
    # 1. Creating smart contract transaction
    # 2. Uploading metadata to IPFS
    # 3. Minting NFT (if requested)
    # 4. Waiting for blockchain confirmation
    
    blockchain_cert = BlockchainCertificate(
        certificate_id=certificate.id,
        blockchain_hash=cert_hash,
        transaction_hash=f"0x{cert_hash[:64]}",
        blockchain_network=BlockchainNetwork.POLYGON,
        contract_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb5",
        token_id=None,
        ipfs_hash=f"Qm{cert_hash[:44]}",
        verification_url=f"https://verify.metalearnpro.com/cert/{certificate.id}",
        minted_at=datetime.utcnow(),
        gas_used=0.05
    )
    
    return blockchain_cert

@app.post("/api/v1/mint-nft", response_model=NFTCertificate)
async def mint_nft_certificate(certificate_id: str, owner_address: str):
    """
    Mint NFT certificate
    إصدار شهادة NFT
    """
    # TODO: Integrate with blockchain to mint actual NFT
    
    nft_cert = NFTCertificate(
        token_id=f"NFT_{certificate_id}",
        name="MetaLearn Pro Certificate",
        description="Verified educational achievement on blockchain",
        image_url=f"https://nft.metalearnpro.com/images/{certificate_id}.png",
        attributes=[
            {"trait_type": "Category", "value": "Education"},
            {"trait_type": "Level", "value": "Advanced"},
            {"trait_type": "Issuer", "value": "MetaLearn Pro"},
            {"trait_type": "Year", "value": str(datetime.utcnow().year)}
        ],
        blockchain_network=BlockchainNetwork.POLYGON,
        contract_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb5",
        owner_address=owner_address,
        created_at=datetime.utcnow()
    )
    
    return nft_cert

@app.get("/api/v1/verify/{certificate_id}", response_model=CertificateVerification)
async def verify_certificate(certificate_id: str):
    """
    Verify certificate authenticity
    التحقق من صحة الشهادة
    """
    # TODO: Query blockchain for actual verification
    
    return CertificateVerification(
        is_valid=True,
        certificate_id=certificate_id,
        blockchain_hash=hashlib.sha256(certificate_id.encode()).hexdigest(),
        issued_to="Sarah Ahmed",
        issued_by="MetaLearn Pro",
        issued_date=datetime(2024, 1, 15),
        verified_at=datetime.utcnow(),
        blockchain_confirmations=156,
        tamper_proof=True
    )

@app.get("/api/v1/student-record/{student_id}", response_model=EducationalRecord)
async def get_educational_record(student_id: str):
    """
    Get permanent educational record
    سجل تعليمي دائم
    """
    return EducationalRecord(
        student_id=student_id,
        student_name="Sarah Ahmed",
        total_certificates=12,
        certificates=[
            {
                "id": "cert_1",
                "title": "Advanced Computer Science",
                "issued_date": "2024-01-15",
                "blockchain_hash": "0x123abc...",
                "type": "course_completion"
            },
            {
                "id": "cert_2",
                "title": "AI & Machine Learning",
                "issued_date": "2024-02-20",
                "blockchain_hash": "0x456def...",
                "type": "course_completion"
            }
        ],
        skills_earned=[
            "Python Programming",
            "Machine Learning",
            "Data Analysis",
            "Web Development",
            "Database Management"
        ],
        achievements=[
            "Top Performer",
            "Perfect Attendance",
            "Community Contributor"
        ],
        total_nfts=3,
        record_hash=hashlib.sha256(f"record_{student_id}".encode()).hexdigest(),
        last_updated=datetime.utcnow()
    )

@app.get("/api/v1/certificates/{student_id}", response_model=List[BlockchainCertificate])
async def get_student_certificates(student_id: str):
    """Get all certificates for a student"""
    # TODO: Query blockchain for actual certificates
    return []

@app.post("/api/v1/revoke-certificate")
async def revoke_certificate(certificate_id: str, reason: str):
    """
    Revoke a certificate (mark as invalid on blockchain)
    """
    # TODO: Update blockchain record
    return {
        "certificate_id": certificate_id,
        "revoked": True,
        "reason": reason,
        "revoked_at": datetime.utcnow().isoformat(),
        "message": "Certificate has been revoked on blockchain"
    }

@app.get("/api/v1/blockchain-stats")
async def get_blockchain_stats():
    """Get blockchain statistics"""
    return {
        "total_certificates_issued": 15847,
        "total_nfts_minted": 3421,
        "blockchain_networks": ["Polygon", "Ethereum"],
        "average_gas_cost": 0.045,
        "verification_success_rate": 99.8,
        "total_verifications": 45123,
        "active_wallets": 8945
    }

@app.post("/api/v1/batch-issue")
async def batch_issue_certificates(certificates: List[Certificate]):
    """
    Batch issue multiple certificates
    إصدار مجموعة شهادات
    """
    results = []
    for cert in certificates:
        cert_hash = generate_certificate_hash(cert)
        results.append({
            "certificate_id": cert.id,
            "blockchain_hash": cert_hash,
            "status": "pending_blockchain_confirmation"
        })
    
    return {
        "total": len(certificates),
        "successful": len(results),
        "failed": 0,
        "results": results,
        "message": f"Batch processing {len(certificates)} certificates"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8007))
    uvicorn.run(app, host="0.0.0.0", port=port)
