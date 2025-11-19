# Task List - Agentic RAG with Knowledge Graph

## Overview
This document tracks all tasks for building the agentic RAG system with knowledge graph capabilities. Tasks are organized by phase and component.

---

## Phase 0: MCP Server Integration & Setup

### External Documentation Gathering
- [X] Use Crawl4AI RAG to get Pydantic AI documentation and examples
- [X] Query documentation for best practices and implementation patterns

### Neon Database Project Setup
- [X] Create new Neon database project using Neon MCP server
- [X] Set up pgvector extension using Neon MCP server
- [X] Create all required tables (documents, chunks, sessions, messages) using Neon MCP server
- [X] Verify table creation using Neon MCP server tools
- [X] Get connection string and update environment configuration
- [X] Test database connectivity and basic operations using Neon MCP server

## Phase 1: Foundation & Setup

### Project Structure
- [x] Create project directory structure
- [x] Set up .gitignore for Python project
- [x] Create .env.example with all required variables
- [x] Initialize virtual environment setup instructions

### Database Setup
- [x] Create PostgreSQL schema with pgvector extension
- [x] Write SQL migration scripts
- [x] Create database connection utilities for PostgreSQL
- [x] Set up connection pooling with asyncpg
- [x] Configure Neo4j connection settings
- [x] Initialize Graphiti client configuration

### Base Models & Configuration
- [x] Create Pydantic models for documents
- [x] Create models for chunks and embeddings
- [x] Create models for search results
- [x] Create models for knowledge graph entities
- [x] Define configuration dataclasses
- [x] Set up logging configuration

---

## Phase 2: Core Agent Development

### Agent Foundation
- [x] Create main agent file with Pydantic AI
- [x] Define agent system prompts
- [x] Set up dependency injection structure
- [x] Configure flexible model settings (OpenAI/Ollama/OpenRouter/Gemini)
- [x] Implement error handling for agent

### RAG Tools Implementation
- [x] Create vector search tool
- [x] Create document metadata search tool
- [x] Create full document retrieval tool
- [x] Implement embedding generation utility
- [x] Add result ranking and formatting
- [x] Create hybrid search orchestration

### Knowledge Graph Tools
- [x] Create graph search tool
- [x] Implement entity lookup tool
- [x] Create relationship traversal tool
- [x] Add temporal filtering capabilities
- [x] Implement graph result formatting
- [x] Create graph visualization data tool

### Tool Integration
- [x] Integrate all tools with main agent
- [x] Create unified search interface
- [x] Implement result merging strategies
- [x] Add context management
- [x] Create tool usage documentation

---

## Phase 3: API Layer

### FastAPI Setup
- [x] Create main FastAPI application
- [x] Configure CORS middleware
- [x] Set up lifespan management
- [x] Add global exception handlers
- [x] Configure logging middleware

### API Endpoints
- [x] Create chat endpoint with streaming
- [x] Implement session management endpoints
- [x] Add document search endpoints
- [x] Create knowledge graph query endpoints
- [x] Add health check endpoint

### Streaming & Real-time
- [x] Implement SSE streaming
- [x] Add delta streaming for responses
- [x] Create connection management
- [x] Handle client disconnections
- [x] Add retry mechanisms

---

## Phase 4: Ingestion System

### Document Processing
- [x] Create markdown file loader
- [x] Implement semantic chunking algorithm
- [x] Research and select chunking strategy
- [x] Add chunk overlap handling
- [x] Create metadata extraction
- [x] Implement document validation

### Embedding Generation
- [x] Create embedding generator class
- [x] Implement batch processing
- [x] Add embedding caching
- [x] Create retry logic for API calls
- [x] Add progress tracking

### Vector Database Insertion
- [x] Create PostgreSQL insertion utilities
- [x] Implement batch insert for chunks
- [x] Add transaction management
- [x] Create duplicate detection
- [x] Implement update strategies

### Knowledge Graph Building
- [x] Create entity extraction pipeline
- [x] Implement relationship detection
- [x] Add Graphiti integration for insertion
- [x] Create temporal data handling
- [x] Implement graph validation
- [x] Add conflict resolution

### Cleanup Utilities
- [x] Create database cleanup script
- [x] Add selective cleanup options
- [x] Implement backup before cleanup
- [x] Create restoration utilities
- [x] Add confirmation prompts

---

## Phase 5: Testing

### Unit Tests - Agent
- [x] Test agent initialization
- [x] Test each tool individually
- [x] Test tool integration
- [x] Test error handling
- [x] Test dependency injection
- [x] Test prompt formatting

### Unit Tests - API
- [x] Test endpoint routing
- [x] Test streaming responses
- [x] Test error responses
- [x] Test session management
- [x] Test input validation
- [x] Test CORS configuration

### Unit Tests - Ingestion
- [x] Test document loading
- [x] Test chunking algorithms
- [x] Test embedding generation
- [x] Test database insertion
- [x] Test graph building
- [x] Test cleanup operations

### Integration Tests
- [x] Test end-to-end chat flow
- [x] Test document ingestion pipeline
- [x] Test search workflows
- [x] Test concurrent operations
- [x] Test database transactions
- [x] Test error recovery

### Test Infrastructure
- [x] Create test fixtures
- [x] Set up database mocks
- [x] Create LLM mocks
- [x] Add test data generators
- [x] Configure test environment

---

## Phase 6: Documentation

### Code Documentation
- [x] Add docstrings to all functions
- [x] Create inline comments for complex logic
- [x] Add type hints throughout
- [x] Create module-level documentation
- [x] Add TODO/FIXME tracking

### User Documentation
- [x] Create comprehensive README
- [x] Write installation guide
- [x] Create usage examples
- [x] Add API documentation
- [x] Create troubleshooting guide
- [x] Add configuration guide

### Developer Documentation
- [x] Create architecture diagrams
- [x] Write contributing guidelines
- [x] Create development setup guide
- [x] Add code style guide
- [x] Create testing guide

---

## Quality Assurance

### Code Quality
- [x] Run black formatter on all code
- [x] Run ruff linter and fix issues
- [x] Check type hints with mypy
- [x] Review code for best practices
- [x] Optimize for performance
- [x] Check for security issues

### Testing & Validation
- [x] Achieve >80% test coverage (58/58 tests passing)
- [x] Run all tests successfully
- [x] Perform manual testing
- [x] Test with real documents
- [x] Validate search results
- [x] Check error handling

### Final Review
- [x] Review all documentation
- [x] Check environment variables
- [x] Validate database schemas
- [x] Test installation process
- [x] Verify all features work
- [x] Create demo scenarios

---

## Critical Fixes

### Code Review & Fixes
- [x] **CRITICAL**: Fix Pydantic AI tool decorators - Remove invalid `description=` parameter
- [x] **CRITICAL**: Implement flexible LLM provider support (OpenAI/Ollama/OpenRouter/Gemini)
- [x] **CRITICAL**: Fix agent streaming implementation using `agent.iter()` pattern
- [x] **CRITICAL**: Move agent execution functions out of agent.py into api.py
- [x] **CRITICAL**: Fix CORS to use `allow_origins=["*"]`
- [x] **CRITICAL**: Update tests to mock all external dependencies (no real DB/API connections)
- [x] Add separate LLM configuration for ingestion (fast/lightweight model option)
- [x] Update .env.example with flexible provider configuration
- [x] Implement proper embedding provider flexibility (OpenAI/Ollama)
- [x] Test and iterate until all tests pass using proper mocking

### Graphiti Integration Fixes
- [x] Fix Graphiti implementation with proper initialization and lifecycle management
- [x] Remove all limit parameters from Graphiti operations per user requirements
- [x] Fix PostgreSQL embedding storage format (JSON string format)
- [x] Remove similarity thresholds entirely from vector search
- [x] Fix ChunkResult UUID to string conversion
- [x] Optimize Graphiti to avoid token limit errors (content truncation)
- [x] Configure Graphiti with OpenAI-compatible clients (OpenAIClient, OpenAIEmbedder)
- [x] Fix duplicate ToolCall model definition in models.py

---

## Phase 7: CLI and Agent Transparency

### Command Line Interface
- [x] Create interactive CLI for agent interaction
- [x] Implement real-time streaming display
- [x] Add tool usage visibility to show agent reasoning
- [x] Create session management in CLI
- [x] Add color-coded output for better readability
- [x] Implement CLI commands (help, health, clear, exit)
- [x] Configure default port to 8058

### API Tool Tracking
- [x] Add ToolCall model for tracking tool usage
- [x] Implement extract_tool_calls function
- [x] Update ChatResponse to include tools_used field
- [x] Add tool usage to streaming responses
- [x] Fix tool call extraction from Pydantic AI messages

### Documentation Updates
- [x] Add CLI usage section to README
- [x] Document agent behavior configuration via prompts.py
- [x] Update model examples to latest versions (gpt-4.1-mini, etc.)
- [x] Update all port references to 8058
- [x] Add note about configuring agent tool selection behavior

---

## Phase 8: BM25 Lexical Search Integration

### BM25S Library Integration (Added 2025-11-17)
- [X] Install bm25s library and dependencies (scipy)
- [X] Create agent/bm25_utils.py module for BM25 indexing and search
- [X] Add BM25Index class with build, save, load, and search methods
- [X] Add BM25 search tool to agent/tools.py
- [X] Register bm25_search tool with the agent in agent/agent.py
- [X] Update hybrid_search_tool to use BM25 instead of PostgreSQL ts_rank
- [X] Update system prompt to mention BM25 and hybrid search capabilities
- [X] Uncomment and activate hybrid_search tool in agent
- [X] Write comprehensive tests for BM25 functionality
- [X] Update requirements.txt with bm25s==0.2.14 and scipy==1.16.3

### BM25 Features
- **BM25 Lexical Search**: Keyword-based search using BM25 algorithm for exact term matching
- **Hybrid Search**: Combines vector embeddings and BM25 scores with weighted ranking
- **Index Persistence**: Automatic saving/loading of BM25 index to disk
- **Database Integration**: Builds index from existing PostgreSQL chunks
- **Three Search Modes**:
  1. Vector search (semantic similarity)
  2. BM25 search (keyword matching)
  3. Hybrid search (best of both worlds)

---

## Phase 9: Langfuse Observability Integration

### Infrastructure Setup (Added 2025-11-19)
- [X] Add Langfuse services to docker-compose.yml (langfuse-db, langfuse-web, langfuse-worker)
- [X] Configure environment variables in .env.example for Langfuse
- [X] Add langfuse to requirements.txt
- [X] Create agent/config.py for centralized configuration management

### Simplified Integration (Pydantic AI Native)
- [X] Add `Agent.instrument_all()` to agent/agent.py for automatic tracing
- [X] Add `@observe()` decorator to chat endpoint in agent/api.py
- [X] Use `propagate_attributes()` for session/user tracking
- [X] Remove over-engineered custom observability module
- [X] Simplify to follow official Pydantic AI + Langfuse pattern

### Testing & Documentation
- [X] Create tests/test_observability.py with basic integration tests
- [X] Update README.md with simplified Langfuse setup instructions
- [X] Update PLANNING.md with observability architecture section
- [X] Document automatic tracing approach

### Langfuse Features (Automatic via Pydantic AI)
- **Zero-Config Tracing**: Automatic tracking of all agent interactions
- **Self-Hosted**: Runs in Docker containers with dedicated PostgreSQL database
- **Session Tracking**: Uses `@observe()` decorator for session correlation
- **Tool Call Tracking**: Automatically captures all tool invocations
- **Token Usage**: Monitors LLM consumption automatically
- **Simple Setup**: Just environment variables - no custom code needed

---

## Project Status

✅ **All core functionality completed and tested**
✅ **58/58 tests passing (+ new BM25 and observability tests)**
✅ **Production ready**
✅ **Comprehensive documentation**
✅ **Flexible provider system implemented**
✅ **CLI with agent transparency features**
✅ **Graphiti integration with OpenAI-compatible clients**
✅ **BM25 lexical search integrated for improved retrieval**
✅ **Langfuse observability for comprehensive tracing and monitoring**

The agentic RAG with knowledge graph system is complete and ready for production use with full observability.

---

## Phase 10: Database Configuration Updates

### PostgreSQL Port Change (Added 2025-11-19)
- [X] Change PostgreSQL port from 5432 to 5433 in docker-compose.yml
- [X] Update DATABASE_URL examples in .env.example to use port 5433
- [X] Update DATABASE_URL examples in PLANNING.md to use port 5433
- [X] Update DATABASE_URL examples in README.md to use port 5433 (no hardcoded port found)

---

## Bug Fixes

### BM25 Search Error When Limit Exceeds Corpus Size (Added 2025-11-19)
- [X] Fix BM25 search to clamp limit parameter to corpus size
- [X] Add empty corpus check before searching
- [X] Add debug logging when limit is clamped
- [X] Add test for search when limit exceeds corpus size
- [X] Add test for search with empty corpus
- [X] Verify all BM25 tests pass (12/12 tests passing)

**Issue**: BM25 search failed with error "k of 10 is larger than the number of available scores" when requesting more results than exist in corpus.

**Solution**: Modified `agent/bm25_utils.py` to clamp the `limit` parameter to `min(limit, len(corpus_data))` before calling `retriever.retrieve()`, preventing the error and gracefully handling small or empty corpora.

### BM25 Metadata JSON Parsing Error (Added 2025-11-19)
- [X] Import json module in bm25_utils.py
- [X] Add JSON parsing for metadata when building BM25 index
- [X] Add error handling for malformed JSON metadata
- [X] Rebuild BM25 index with 445 chunks successfully
- [X] Verify all BM25 tests pass (12/12 tests passing)

**Issue**: BM25 search failed with Pydantic validation error: "Input should be a valid dictionary [type=dict_type]" for the `metadata` field. PostgreSQL JSONB field was being stored as a JSON string in the BM25 index, but `ChunkResult` model expects a dictionary.

**Solution**: Modified `agent/bm25_utils.py` to parse metadata JSON strings to dictionaries when building the index (line ~102-108), matching the behavior in `agent/db_utils.py`. Added safe parsing with error handling to gracefully handle malformed JSON by using an empty dict fallback.