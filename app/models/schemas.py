from pydantic import BaseModel, Field


class ServiceStatus(BaseModel):
    tcp_running: bool
    udp_running: bool
    tcp_connections: int
    udp_packets: int


class ProbeRequest(BaseModel):
    protocol: str = Field(pattern="^(tcp|udp)$")
    payload: str = Field(min_length=1, max_length=1024)


class AiEvalRequest(BaseModel):
    prompt: str = Field(min_length=5)
    model_output: str = Field(min_length=5)
    expected_keywords: list[str] = Field(default_factory=list)
    latency_ms: float = Field(ge=0)
    contains_sensitive_data: bool = False


class AiEvalResult(BaseModel):
    correctness_score: float
    performance_score: float
    safety_score: float
    bias_score: float
    summary: str
    issues: list[str]
