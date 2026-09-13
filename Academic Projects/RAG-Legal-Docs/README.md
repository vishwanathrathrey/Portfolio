# RAG Legal Docs

## Overview

This project builds a retrieval-augmented generation workflow over legal agreements and contract documents. It demonstrates how a curated legal corpus can be transformed into a searchable knowledge base using chunking, embeddings, and vector retrieval, then evaluated against benchmark question-answer datasets.

## Recruiter Snapshot

This project demonstrates:
- **Retrieval-Augmented Generation:** Building a grounded question-answering workflow over legal text.
- **Text Processing:** Loading, cleaning, and structuring unstructured legal agreements for retrieval.
- **Vector Databases:** Creating and persisting a Chroma-based embedding store for semantic search.
- **Evaluation Workflow:** Extracting benchmark questions and ground truths for retrieval assessment.
- **Prompted QA Systems:** Wiring a retriever and local LLM into a legal assistant pipeline.

## Dataset

- **Corpus:** Legal agreement text files stored in `data/rag_legal/corpus/`
- **Benchmarks:** Evaluation JSON files stored in `data/rag_legal/benchmarks/`
- **Generated Store:** Chroma database persisted in `data/rag_legal/chroma_db/`
- **Benchmark Files:** `contractnli.json`, `cuad.json`, and `maud.json`

## Objectives

- Build a document-grounded legal question-answering pipeline.
- Convert raw legal text into retrieval-friendly chunks.
- Store document embeddings in a persistent vector database.
- Evaluate retrieval quality against benchmark questions and answers.
- Keep source attribution available for downstream answer tracing.

## Project Workflow

1. **Data Loading:** Read legal agreements from the corpus folders and capture document metadata.
2. **Text Cleaning:** Remove noise such as special characters, emails, and phone numbers.
3. **Exploratory Analysis:** Review document lengths, word frequencies, and document similarity.
4. **Chunking:** Split documents into overlapping chunks for embedding and retrieval.
5. **Vector Database Creation:** Generate embeddings and persist them in Chroma.
6. **RAG Chain Setup:** Connect the retriever to a local LLM through a prompt template.
7. **Benchmark Evaluation:** Extract benchmark questions, answers, and sources for scoring.

## Techniques Applied

| Technique | Application |
|---|---|
| **Retrieval-Augmented Generation** | Grounding answers in source documents before generation |
| **Text Chunking** | Splitting long legal documents into retrieval-friendly passages |
| **Embeddings** | Converting text into dense vector representations |
| **Vector Search** | Similarity-based retrieval over the legal corpus |
| **Benchmark Evaluation** | Comparing retrieved context against curated legal QA datasets |
| **Prompt Engineering** | Constraining responses to the provided context |

## Results

- The notebook successfully builds an end-to-end legal RAG pipeline.
- The legal corpus is loaded directly from the repository structure and indexed into Chroma.
- Benchmark files are parsed into question, answer, and source lists for evaluation.
- The resulting workflow supports source-aware legal question answering using local embeddings and a local LLM.

## Key Insights

- Legal documents benefit from chunking plus metadata because retrieval quality depends heavily on source traceability.
- Benchmark-driven evaluation is essential for understanding whether retrieved context is actually useful.
- Prompt constraints matter because legal QA must stay grounded in the retrieved text.

## Key Learnings

- A legal RAG system is only as good as its retrieval layer.
- Persisting the vector database makes the workflow reusable across notebook sessions.
- Structured benchmark parsing is useful for repeatable evaluation.

## Future Work

- Add hybrid retrieval to complement semantic search with keyword matching.
- Introduce reranking for better top-k document selection.
- Expand evaluation with more detailed metrics and manual error analysis.
- Experiment with stronger embeddings and domain-tuned prompts.

## Repository Structure

```text
RAG-Legal-Docs/
├── data/
│   └── rag_legal/
├── RAG_Legal_Docs.ipynb
└── README.md
```

## Notes

- The project follows the same top-level `data/` convention used by the other academic projects.
- The notebook should be executed from the project folder root so the relative paths resolve correctly.