# Claude Code MCP Server Configuration

이 프로젝트에서 사용하는 MCP (Model Context Protocol) 서버 설정입니다.

## 설정된 MCP 서버

### KIS Code Assistant

**제공자:** 한국투자증권 (Korea Investment & Securities)
**URL:** https://server.smithery.ai/@KISOpenAPI/kis-code-assistant-mcp/mcp

**기능:**
- 한국투자증권 Open API 검색
- 자연어로 API 찾기
- 자동 코드 생성 예제 제공

**사용 가능한 도구:**

1. `search_auth_api` - 인증 관련 API (토큰 발급, WebSocket 연결)
2. `search_domestic_stock_api` - 국내 주식 API (시세, 순위, 실시간 호가)
3. `search_domestic_bond_api` - 국내 채권 API
4. `search_domestic_futureoption_api` - 국내 선물/옵션 API
5. `search_overseas_stock_api` - 해외 주식 API
6. `search_overseas_futureoption_api` - 해외 선물/옵션 API
7. `search_elw_api` - ELW 관련 API
8. 추가 기능 - 뉴스, 지수, 섹터 분석 등

## 사용 방법

### 1. Claude Code에서 자동 인식

이 프로젝트 디렉토리에서 Claude Code를 실행하면 자동으로 `.claude/mcp.json` 파일을 읽어서 MCP 서버를 연결합니다.

### 2. MCP 도구 사용 예시

```
사용자: "국내 주식 현재가 조회하는 API를 찾아줘"
Assistant: [search_domestic_stock_api 도구를 사용하여 관련 API 검색]
```

```
사용자: "토큰 발급하는 방법 알려줘"
Assistant: [search_auth_api 도구를 사용하여 인증 API 정보 제공]
```

## MCP 서버 추가/수정

프로젝트에 새로운 MCP 서버를 추가하려면 `.claude/mcp.json` 파일을 편집하세요:

```json
{
  "mcpServers": {
    "kis-code-assistant": {
      "url": "https://server.smithery.ai/@KISOpenAPI/kis-code-assistant-mcp/mcp",
      "description": "KIS Open API Code Assistant"
    },
    "새로운-서버": {
      "url": "https://example.com/mcp",
      "description": "설명"
    }
  }
}
```

## 참고 자료

- **Smithery 페이지:** https://smithery.ai/server/@KISOpenAPI/kis-code-assistant-mcp
- **KIS Open API GitHub:** https://github.com/koreainvestment/open-trading-api
- **MCP 프로토콜 문서:** https://modelcontextprotocol.io/

## 문제 해결

### MCP 서버가 연결되지 않을 때

1. 인터넷 연결 확인
2. `.claude/mcp.json` 파일 문법 확인 (유효한 JSON인지)
3. Claude Code 재시작

### MCP 도구가 보이지 않을 때

Claude Code가 프로젝트 루트 디렉토리에서 실행되고 있는지 확인하세요.

```bash
# 현재 위치 확인
pwd
# /Users/diveangel/Works/exodus-trading-system

# .claude 디렉토리 확인
ls -la .claude/
```

---

**Last Updated:** 2025-11-03
