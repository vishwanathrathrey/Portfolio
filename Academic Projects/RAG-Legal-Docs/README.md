# RAG Legal Docs

## Overview

This project builds a retrieval-augmented generation workflow over legal agreements and contract documents. The notebook focuses on ingesting a curated legal corpus under a top-level `data/` folder, chunking the text, creating embeddings, storing them in a Chroma vector database, and evaluating retrieval against benchmark question-answer datasets.

## Dataset

- **Corpus:** Legal agreement text files stored in `data/rag_legal/corpus/`
- **Benchmarks:** Evaluation JSON files stored in `data/rag_legal/benchmarks/`
- **Generated Store:** Chroma database persisted in `data/rag_legal/chroma_db/`
- **Benchmark Files:** `contractnli.json`, `cuad.json`, and `maud.json`

## What the notebook covers

1. Load and inspect the legal corpus and benchmark files.
2. Clean and prepare text for retrieval.
3. Chunk documents for embedding and similarity search.
4. Build and persist a Chroma vector store.
5. Extract benchmark questions and answers for evaluation.
6. Measure retrieval quality on legal question-answer pairs.

## Techniques and Concepts

| Technique | Application |
|---|---|
| **Retrieval-Augmented Generation** | Grounding answers in source documents before generation |
| **Text Chunking** | Splitting long legal documents into retrieval-friendly passages |
| **Embeddings** | Converting text into dense vector representations |
| **Vector Search** | Similarity-based retrieval over the legal corpus |
| **Benchmark Evaluation** | Comparing retrieved context against curated legal QA datasets |

## Repository Structure

```text
RAG-Legal-Docs/
├── data/
│   └── rag_legal/
├── RAG_Legal_Docs.ipynb
└── README.md
```

## Notes

- The project now follows the same top-level `data/` convention used by the other academic projects.
- The notebook uses relative paths, so it should be run from the project folder root.